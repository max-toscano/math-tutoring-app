/**
 * Supabase client — configured for React Native / Expo.
 *
 * Env vars (set in .env):
 *   EXPO_PUBLIC_SUPABASE_URL
 *   EXPO_PUBLIC_SUPABASE_ANON_KEY
 */
import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';
import { Platform } from 'react-native';
import type { Database } from './database.types';

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error(
    'Missing EXPO_PUBLIC_SUPABASE_URL or EXPO_PUBLIC_SUPABASE_ANON_KEY. Add them to your .env file.',
  );
}

// AsyncStorage only works in a client environment (not during SSR)
let storage: any = undefined;
if (typeof window !== 'undefined') {
  // Dynamic import to avoid SSR issues with AsyncStorage
  storage = require('@react-native-async-storage/async-storage').default;
}

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey, {
  auth: {
    storage,
    autoRefreshToken: true,
    persistSession: typeof window !== 'undefined',
    // On web: true — Supabase auto-reads tokens from the URL fragment (#access_token=...)
    //   when the user clicks the password-reset email link and gets redirected back.
    // On mobile: false — React Native doesn't have browser-style URLs,
    //   so we handle deep links manually in _layout.tsx instead.
    detectSessionInUrl: Platform.OS === 'web',
  },
});
