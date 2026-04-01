import { useEffect } from 'react';
import { useRouter, useSegments, Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import * as Linking from 'expo-linking';
import { AppProvider, useAppContext } from '../context/AppContext';
import { Colors } from '../constants/Colors';
import { supabase } from '../lib/supabase';

// ════════════════════════════════════════════════════════════════════════════
// AuthGate
// ════════════════════════════════════════════════════════════════════════════
//
// This component is the "bouncer" of your app. It runs on every navigation
// and decides: should this user be allowed on this screen?
//
// The logic is simple:
//   • Not logged in + trying to access app screens → redirect to login
//   • Logged in + on an auth screen → redirect to the main app (tabs)
//
// The new addition: PASSWORD RECOVERY.
// When a user clicks a password-reset email link, they become "logged in"
// (Supabase gives them a session). But we DON'T want to send them to the
// main app — we want them on the reset-password screen. So we check
// isRecoveringPassword and skip the redirect if it's true.
//

function AuthGate() {
  const { user, authLoading, isRecoveringPassword } = useAppContext();
  const segments = useSegments();
  const router = useRouter();

  // ── Deep link handler ────────────────────────────────────────────────
  //
  // WHAT THIS DOES:
  // When the user clicks the password-reset link in their email, the
  // browser/OS opens your app via a deep link URL like:
  //
  //   mathhelper://reset-password#access_token=eyJ...&refresh_token=abc&type=recovery
  //
  // The tokens are in the URL "fragment" (everything after the #).
  // We need to:
  //   1. Catch this URL when it arrives
  //   2. Parse out the access_token and refresh_token
  //   3. Give them to Supabase via setSession()
  //   4. Supabase then fires the 'PASSWORD_RECOVERY' event
  //   5. AppContext catches that event and sets isRecoveringPassword = true
  //   6. We navigate to the reset-password screen
  //
  // WHY WE DO THIS MANUALLY:
  // In supabase.ts, detectSessionInUrl is set to false. This is correct
  // for React Native (RN doesn't have browser-style URL detection).
  // But it means we must manually extract tokens from deep link URLs.
  //
  // TWO SCENARIOS TO HANDLE:
  //   a) App is already open → Linking.addEventListener fires
  //   b) App was closed → Linking.getInitialURL() returns the launch URL
  //
  useEffect(() => {
    // Parse a deep-link URL and extract recovery tokens if present
    async function handleDeepLink(url: string) {
      // The URL might look like:
      //   mathhelper://reset-password#access_token=eyJ...&refresh_token=abc&type=recovery
      //
      // Split on '#' to get the fragment, then parse it as URL search params.
      // URL fragments use the same key=value&key=value format as query strings,
      // so URLSearchParams works perfectly.
      const fragment = url.split('#')[1];
      if (!fragment) return; // No fragment → not a recovery link

      const params = new URLSearchParams(fragment);
      const accessToken = params.get('access_token');
      const refreshToken = params.get('refresh_token');
      const type = params.get('type');

      // Only proceed if this is a recovery link with valid tokens
      if (type === 'recovery' && accessToken && refreshToken) {
        // Hand the tokens to Supabase. This does two things:
        //   1. Creates a valid session (user is now "logged in")
        //   2. Fires onAuthStateChange with event='PASSWORD_RECOVERY'
        //      (which AppContext catches to set isRecoveringPassword=true)
        const { error } = await supabase.auth.setSession({
          access_token: accessToken,
          refresh_token: refreshToken,
        });

        if (!error) {
          // Navigate to the screen where they'll type their new password
          router.replace('/(auth)/reset-password');
        }
      }
    }

    // Scenario A: App is already running, user taps the email link.
    // Linking.addEventListener fires with the URL.
    const subscription = Linking.addEventListener('url', (event) => {
      handleDeepLink(event.url);
    });

    // Scenario B: App was closed, user taps the email link to launch it.
    // The launch URL is available via getInitialURL().
    Linking.getInitialURL().then((url) => {
      if (url) handleDeepLink(url);
    });

    // Cleanup: remove the listener when this component unmounts
    return () => subscription.remove();
  }, [router]);

  // ── Auth gate logic ──────────────────────────────────────────────────
  useEffect(() => {
    if (authLoading) return;

    // segments[0] tells us which route group we're in.
    // '(auth)' = login, signup, forgot-password, reset-password screens
    // '(tabs)' = the main app screens
    const inAuthGroup = segments[0] === '(auth)';

    // ── Recovery mode: highest priority ──
    // If the PASSWORD_RECOVERY event fired (user clicked the email link),
    // send them straight to the reset-password screen no matter where they
    // currently are. This handles BOTH web and mobile:
    //   - Web: Supabase auto-detected tokens in URL (detectSessionInUrl: true)
    //          → fired PASSWORD_RECOVERY → isRecoveringPassword became true
    //   - Mobile: deep link handler parsed the URL → called setSession()
    //          → PASSWORD_RECOVERY event fired → isRecoveringPassword became true
    //
    // We check if they're already on the reset-password screen to avoid
    // an infinite redirect loop (replace → triggers segments change → re-runs effect).
    if (isRecoveringPassword) {
      const alreadyOnResetScreen = segments.join('/').includes('reset-password');
      if (!alreadyOnResetScreen) {
        router.replace('/(auth)/reset-password');
      }
      return; // Don't run the normal auth gate logic below
    }

    if (!user && !inAuthGroup) {
      // Not signed in and trying to access the app → send to login
      router.replace('/(auth)/login');
    } else if (user && inAuthGroup) {
      // Signed in + on an auth screen + recovery is done → go to app.
      router.replace('/(tabs)');
    }
  }, [user, authLoading, segments, isRecoveringPassword]);

  if (authLoading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color={Colors.primary} />
      </View>
    );
  }

  return (
    <>
      <Stack screenOptions={{ headerShown: false }} />
      <StatusBar style="light" />
    </>
  );
}

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <AppProvider>
        <AuthGate />
      </AppProvider>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.background,
  },
});
