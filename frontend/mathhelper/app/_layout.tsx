import '../lib/amplify'; // Initialize Amplify before any auth calls
import { useEffect } from 'react';
import { useRouter, useSegments, Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { AppProvider, useAppContext } from '../context/AppContext';
import { Colors } from '../constants/Colors';

// ════════════════════════════════════════════════════════════════════════════
// AuthGate
// ════════════════════════════════════════════════════════════════════════════
//
// This component is the "bouncer" of your app. It runs on every navigation
// and decides: should this user be allowed on this screen?
//
//   • Not logged in + trying to access app screens → redirect to login
//   • Logged in + on an auth screen → redirect to the main app (tabs)
//

function AuthGate() {
  const { user, authLoading } = useAppContext();
  const segments = useSegments();
  const router = useRouter();

  // ── Auth gate logic ──────────────────────────────────────────────────
  //
  // Runs on every navigation. Two rules:
  //   • Not signed in + trying to access app screens → redirect to login
  //   • Signed in + on an auth screen → redirect to main tabs
  //
  // Cognito's password reset is code-based (no deep links), so there is
  // no recovery session to intercept here. The forgot-password screen
  // navigates directly to reset-password with the email as a param.
  //
  useEffect(() => {
    if (authLoading) return;

    const inAuthGroup = segments[0] === '(auth)';

    if (!user && !inAuthGroup) {
      router.replace('/(auth)/login');
    } else if (user && inAuthGroup) {
      router.replace('/(tabs)');
    }
  }, [user, authLoading, segments]);

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
