import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
// MathAnalysis and Message types inlined (old services deleted)
export interface MathAnalysis {
  problem: string;
  topic: string;
  subject_area: string;
  difficulty: string;
  answer: string;
  method: string;
  steps: { step: number; title: string; math?: string; explanation: string; note?: string }[];
  verification?: string;
  concepts: string[];
  prerequisites: string[];
  common_mistakes: string[];
  tip?: string;
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}
import type { Session, User } from '../services/auth';
import { onAuthStateChange, getSession as getAuthSession } from '../services/auth';
import * as db from '../services/database';
import { uploadImage, getImageUrl } from '../services/storage';

const STORAGE_KEY = '@mathhelper_saved_v1';
const SESSIONS_KEY = '@mathhelper_sessions_v1';
const MIGRATED_KEY = '@mathhelper_migrated_to_supabase';

// ─── Public types (unchanged — existing screens keep working) ───────────────

export interface SavedItem {
  id: string;
  imageUri: string;
  analysis: MathAnalysis;
  savedAt: string;
}

export interface SessionMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  imageUri?: string;
}

export interface TutoringSession {
  id: string;
  title: string;
  preview: string;
  messages: SessionMessage[];
  conversationHistory: Message[];
  analysis?: MathAnalysis;
  photoUri?: string;
  savedAt: string;
  updatedAt: string;
}

// ─── Context ─────────────────────────────────────────────────────────────────

interface AppContextValue {
  // Auth
  user: User | null;
  session: Session | null;
  authLoading: boolean;

  // Saved items
  savedItems: SavedItem[];
  isLoading: boolean;
  saveAnalysis: (rawImageUri: string, analysis: MathAnalysis) => Promise<void>;
  deleteItem: (id: string) => Promise<void>;

  // Tutoring sessions
  sessions: TutoringSession[];
  saveSession: (session: Omit<TutoringSession, 'id' | 'savedAt' | 'updatedAt'>) => Promise<string>;
  updateSession: (id: string, updates: Partial<Pick<TutoringSession, 'title' | 'messages' | 'conversationHistory' | 'analysis' | 'photoUri'>>) => Promise<void>;
  deleteSession: (id: string) => Promise<void>;
  getSession: (id: string) => TutoringSession | undefined;
}

const AppContext = createContext<AppContextValue | null>(null);

// ─── Provider ────────────────────────────────────────────────────────────────

export function AppProvider({ children }: { children: ReactNode }) {
  // Auth state
  const [user, setUser] = useState<User | null>(null);
  const [authSession, setAuthSession] = useState<Session | null>(null);
  const [authLoading, setAuthLoading] = useState(true);

  // Data state
  const [savedItems, setSavedItems] = useState<SavedItem[]>([]);
  const [sessions, setSessions] = useState<TutoringSession[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // ── Auth listener ──────────────────────────────────────────────────────
  //
  // Runs once on app start. Does two things:
  //   1. getAuthSession() — restores an existing Cognito session from
  //      Amplify's AsyncStorage cache (keeps user logged in between launches)
  //   2. onAuthStateChange() — listens for signedIn / signedOut / tokenRefresh
  //      events from Cognito via Amplify Hub and updates state accordingly
  //
  useEffect(() => {
    getAuthSession().then((session) => {
      setAuthSession(session);
      setUser(session?.user ?? null);
      setAuthLoading(false);
    });

    const subscription = onAuthStateChange((event, session) => {
      setAuthSession(session);
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  // ── Load data when user changes ──
  useEffect(() => {
    if (!user) {
      setSavedItems([]);
      setSessions([]);
      setIsLoading(false);
      return;
    }

    let cancelled = false;
    setIsLoading(true);

    (async () => {
      try {
        // Migrate local data on first login
        await migrateLocalData(user.id);

        // Fetch from Supabase
        const [items, sess] = await Promise.all([
          db.fetchSavedItems(),
          db.fetchSessions(),
        ]);

        if (!cancelled) {
          const resolvedItems = await resolveImageUrls(items);
          const resolvedSessions = await resolveSessionImageUrls(sess);
          setSavedItems(resolvedItems);
          setSessions(resolvedSessions);
        }
      } catch (err) {
        console.error('Failed to load data from Supabase:', err);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();

    return () => { cancelled = true; };
  }, [user]);

  // ── Saved Items ──

  const saveAnalysis = useCallback(
    async (rawImageUri: string, analysis: MathAnalysis) => {
      if (!user) throw new Error('Must be signed in');

      const storagePath = await uploadImage(user.id, rawImageUri);
      const signedUrl = await getImageUrl(storagePath);
      const newItem = await db.insertSavedItem(user.id, storagePath, analysis);

      setSavedItems((prev) => [{ ...newItem, imageUri: signedUrl }, ...prev]);
    },
    [user],
  );

  const deleteItem = useCallback(
    async (id: string) => {
      await db.deleteSavedItem(id);
      setSavedItems((prev) => prev.filter((i) => i.id !== id));
    },
    [],
  );

  // ── Tutoring Sessions ──

  const saveSession = useCallback(
    async (session: Omit<TutoringSession, 'id' | 'savedAt' | 'updatedAt'>): Promise<string> => {
      if (!user) throw new Error('Must be signed in');

      let photoUrl: string | undefined;
      if (session.photoUri) {
        try {
          photoUrl = await uploadImage(user.id, session.photoUri);
        } catch {
          // Keep going without photo
        }
      }

      const messages: SessionMessage[] = await Promise.all(
        session.messages.map(async (msg) => {
          if (msg.imageUri) {
            try {
              const imgPath = await uploadImage(user.id, msg.imageUri);
              return { ...msg, imageUri: imgPath };
            } catch {
              return msg;
            }
          }
          return msg;
        }),
      );

      const sessionId = await db.insertSession(user.id, {
        title: session.title,
        preview: session.preview,
        messages,
        analysis: session.analysis,
        photoUrl,
      });

      // Refresh from server
      const allSessions = await db.fetchSessions();
      const resolved = await resolveSessionImageUrls(allSessions);
      setSessions(resolved);

      return sessionId;
    },
    [user],
  );

  const updateSession = useCallback(
    async (id: string, updates: Partial<Pick<TutoringSession, 'title' | 'messages' | 'conversationHistory' | 'analysis' | 'photoUri'>>) => {
      if (!user) throw new Error('Must be signed in');

      let processedMessages: SessionMessage[] | undefined;
      if (updates.messages) {
        processedMessages = await Promise.all(
          updates.messages.map(async (msg) => {
            // Only upload images that are local URIs (not already signed URLs)
            if (msg.imageUri && !msg.imageUri.startsWith('http')) {
              try {
                const imgPath = await uploadImage(user.id, msg.imageUri);
                return { ...msg, imageUri: imgPath };
              } catch {
                return msg;
              }
            }
            return msg;
          }),
        );
      }

      await db.updateSession(id, {
        title: updates.title,
        messages: processedMessages,
        analysis: updates.analysis,
        photoUrl: updates.photoUri,
      });

      // Refresh from server for consistent URLs
      const allSessions = await db.fetchSessions();
      const resolved = await resolveSessionImageUrls(allSessions);
      setSessions(resolved);
    },
    [user],
  );

  const deleteSession = useCallback(
    async (id: string) => {
      await db.deleteSession(id);
      setSessions((prev) => prev.filter((s) => s.id !== id));
    },
    [],
  );

  const getSessionById = useCallback(
    (id: string) => sessions.find((s) => s.id === id),
    [sessions],
  );

  return (
    <AppContext.Provider
      value={{
        user,
        session: authSession,
        authLoading,
        savedItems,
        isLoading,
        saveAnalysis,
        deleteItem,
        sessions,
        saveSession,
        updateSession,
        deleteSession,
        getSession: getSessionById,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext(): AppContextValue {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useAppContext must be used within <AppProvider>');
  return ctx;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

async function resolveImageUrls(items: SavedItem[]): Promise<SavedItem[]> {
  return Promise.all(
    items.map(async (item) => {
      try {
        const signedUrl = await getImageUrl(item.imageUri);
        return { ...item, imageUri: signedUrl };
      } catch {
        return item;
      }
    }),
  );
}

async function resolveSessionImageUrls(sessions: TutoringSession[]): Promise<TutoringSession[]> {
  return Promise.all(
    sessions.map(async (session) => {
      let photoUri = session.photoUri;
      if (photoUri) {
        try {
          photoUri = await getImageUrl(photoUri);
        } catch {
          // Keep original
        }
      }

      const messages = await Promise.all(
        session.messages.map(async (msg) => {
          if (msg.imageUri) {
            try {
              return { ...msg, imageUri: await getImageUrl(msg.imageUri) };
            } catch {
              return msg;
            }
          }
          return msg;
        }),
      );

      return { ...session, photoUri, messages };
    }),
  );
}

// ─── Migration: AsyncStorage → Supabase (one-time on first login) ───────────

async function migrateLocalData(userId: string) {
  try {
    const alreadyMigrated = await AsyncStorage.getItem(MIGRATED_KEY);
    if (alreadyMigrated) return;

    const [rawItems, rawSessions] = await Promise.all([
      AsyncStorage.getItem(STORAGE_KEY),
      AsyncStorage.getItem(SESSIONS_KEY),
    ]);

    const localItems: SavedItem[] = rawItems ? JSON.parse(rawItems) : [];
    const localSessions: TutoringSession[] = rawSessions ? JSON.parse(rawSessions) : [];

    if (localItems.length === 0 && localSessions.length === 0) {
      await AsyncStorage.setItem(MIGRATED_KEY, 'true');
      return;
    }

    console.log(`Migrating ${localItems.length} saved items and ${localSessions.length} sessions to Supabase...`);

    // Migrate saved items
    for (const item of localItems) {
      try {
        let storagePath: string;
        try {
          storagePath = await uploadImage(userId, item.imageUri);
        } catch {
          storagePath = `${userId}/migrated_${item.id}.jpg`;
        }
        await db.insertSavedItem(userId, storagePath, item.analysis);
      } catch (err) {
        console.warn('Failed to migrate saved item:', item.id, err);
      }
    }

    // Migrate sessions
    for (const session of localSessions) {
      try {
        let photoUrl: string | undefined;
        if (session.photoUri) {
          try {
            photoUrl = await uploadImage(userId, session.photoUri);
          } catch {
            // Skip photo
          }
        }

        const messages: SessionMessage[] = [];
        for (const msg of session.messages) {
          if (msg.imageUri) {
            try {
              const imgPath = await uploadImage(userId, msg.imageUri);
              messages.push({ ...msg, imageUri: imgPath });
            } catch {
              messages.push({ ...msg, imageUri: undefined });
            }
          } else {
            messages.push(msg);
          }
        }

        await db.insertSession(userId, {
          title: session.title,
          preview: session.preview,
          messages,
          analysis: session.analysis,
          photoUrl,
        });
      } catch (err) {
        console.warn('Failed to migrate session:', session.id, err);
      }
    }

    // Mark migrated — local data is kept as a safety net
    await AsyncStorage.setItem(MIGRATED_KEY, 'true');
    console.log('Migration to Supabase complete.');
  } catch (err) {
    console.error('Migration failed:', err);
  }
}
