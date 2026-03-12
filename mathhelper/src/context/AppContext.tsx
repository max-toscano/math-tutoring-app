import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';
import type { MathAnalysis } from '../services/openai';

const STORAGE_KEY = '@mathhelper_saved_v1';

export interface SavedItem {
  id: string;
  /** data URL (web) or absolute file path (native) */
  imageUri: string;
  analysis: MathAnalysis;
  savedAt: string;
}

interface AppContextValue {
  savedItems: SavedItem[];
  isLoading: boolean;
  saveAnalysis: (rawImageUri: string, analysis: MathAnalysis) => Promise<void>;
  deleteItem: (id: string) => Promise<void>;
}

const AppContext = createContext<AppContextValue | null>(null);

// Converts a temporary image URI into a form that survives the session.
// Web  → fetch blob and return a data URL (stored in AsyncStorage / localStorage).
// Native → copy file to the app's permanent document directory.
async function makePersistentUri(uri: string): Promise<string> {
  if (Platform.OS === 'web') {
    const res = await fetch(uri);
    const blob = await res.blob();
    return new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  } else {
    const FS = await import('expo-file-system');
    const ext = uri.split('.').pop()?.split('?')[0] ?? 'jpg';
    const dest = `${FS.documentDirectory}mathhelper_${Date.now()}.${ext}`;
    await FS.copyAsync({ from: uri, to: dest });
    return dest;
  }
}

async function removePersistedFile(uri: string) {
  if (Platform.OS !== 'web' && uri.startsWith('/')) {
    const FS = await import('expo-file-system');
    await FS.deleteAsync(uri, { idempotent: true }).catch(() => {});
  }
}

export function AppProvider({ children }: { children: ReactNode }) {
  const [savedItems, setSavedItems] = useState<SavedItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load from storage on mount
  useEffect(() => {
    AsyncStorage.getItem(STORAGE_KEY)
      .then((raw) => {
        if (raw) setSavedItems(JSON.parse(raw));
      })
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, []);

  const persist = useCallback(async (items: SavedItem[]) => {
    setSavedItems(items);
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  }, []);

  const saveAnalysis = useCallback(
    async (rawImageUri: string, analysis: MathAnalysis) => {
      const imageUri = await makePersistentUri(rawImageUri);
      const newItem: SavedItem = {
        id: `${Date.now()}_${Math.random().toString(36).slice(2)}`,
        imageUri,
        analysis,
        savedAt: new Date().toISOString(),
      };
      await persist([newItem, ...savedItems]);
    },
    [savedItems, persist]
  );

  const deleteItem = useCallback(
    async (id: string) => {
      const item = savedItems.find((i) => i.id === id);
      if (item) await removePersistedFile(item.imageUri);
      await persist(savedItems.filter((i) => i.id !== id));
    },
    [savedItems, persist]
  );

  return (
    <AppContext.Provider value={{ savedItems, isLoading, saveAnalysis, deleteItem }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext(): AppContextValue {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useAppContext must be used within <AppProvider>');
  return ctx;
}
