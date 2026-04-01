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
import { Platform } from 'react-native';
import type { Session, User } from '../services/auth';
import { onAuthStateChange, getSession as getAuthSession } from '../services/auth';
// ↑ We import onAuthStateChange which now passes the event type
// (e.g. 'PASSWORD_RECOVERY') along with the session. See auth.ts.
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

  // Password recovery mode
  // ──────────────────────────────────────────────────────────────────
  // When the user clicks a password-reset link in their email, Supabase
  // gives them a valid session (they're technically "logged in"). But we
  // DON'T want to send them to the main app — we want to send them to
  // the reset-password screen so they can type a new password.
  //
  // This flag tells the auth gate: "yes this user has a session, but
  // they're in the middle of resetting their password — don't redirect
  // them to the tabs."
  //
  // clearPasswordRecovery() is called after they successfully set their
  // new password, which lets the auth gate redirect them normally.
  isRecoveringPassword: boolean;
  clearPasswordRecovery: () => void;

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

  // Password recovery flag — see the interface comment above for explanation.
  //
  // THE FIX: We check the URL hash RIGHT HERE, in the initial useState call,
  // not in an async event listener. Here's why:
  //
  // When the user clicks the email link, the browser navigates to something like:
  //   http://localhost:8081/reset-password#access_token=eyJ...&type=recovery
  //
  // The page loads fresh. Supabase's createClient() runs (in supabase.ts) and
  // sees detectSessionInUrl=true, so it reads the URL hash, finds the tokens,
  // and fires the PASSWORD_RECOVERY event. BUT — this all happens BEFORE React
  // mounts any components and BEFORE our onAuthStateChange listener is registered.
  //
  // So the event fires into the void — nobody catches it. By the time our
  // listener is ready, the event already happened. The auth gate sees a logged-in
  // user and sends them to tabs.
  //
  // The solution: check window.location.hash SYNCHRONOUSLY in the initial state.
  // useState(initialValue) runs during the very first render, before any effects.
  // If the URL contains "type=recovery", we start with isRecoveringPassword=true,
  // so the auth gate NEVER gets a chance to redirect to tabs.
  //
  // This only applies to web — on mobile, deep links are handled differently
  // (via Linking.addEventListener in _layout.tsx).
  //
  const [isRecoveringPassword, setIsRecoveringPassword] = useState(() => {
    if (Platform.OS === 'web' && typeof window !== 'undefined') {
      return window.location.hash.includes('type=recovery');
    }
    return false;
  });
  const clearPasswordRecovery = useCallback(() => setIsRecoveringPassword(false), []);

  // Data state
  const [savedItems, setSavedItems] = useState<SavedItem[]>([]);
  const [sessions, setSessions] = useState<TutoringSession[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // ── Auth listener ──────────────────────────────────────────────────────
  //
  // This runs once when the app starts. It does two things:
  //
  //   1. getAuthSession() — checks if there's a saved session from a
  //      previous app launch (stored in AsyncStorage). If yes, the user
  //      is still logged in without needing to re-enter credentials.
  //
  //   2. onAuthStateChange() — subscribes to future auth events. Whenever
  //      the user signs in, signs out, or clicks a password-reset link,
  //      this callback fires with the event name and new session.
  //
  //      We now check for the 'PASSWORD_RECOVERY' event specifically.
  //      When detected, we set isRecoveringPassword = true, which tells
  //      the AuthGate in _layout.tsx to let the user stay on the
  //      reset-password screen instead of redirecting to the main app.
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

      // Detect password recovery — user clicked the reset link in their email.
      // Supabase fires 'PASSWORD_RECOVERY' after exchanging the recovery
      // token for a full session. We flip the flag so the auth gate knows
      // to keep the user on the reset-password screen.
      if (event === 'PASSWORD_RECOVERY') {
        setIsRecoveringPassword(true);
      }
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
        isRecoveringPassword,
        clearPasswordRecovery,
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
