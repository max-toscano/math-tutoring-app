# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the frontend React Native (Expo) application for MathHelper, an AI-powered math tutoring app. The app allows students to scan math problems, chat with an AI tutor, and save their work. It uses Supabase for authentication and data storage, and communicates with a Python backend API for AI tutoring functionality.

## Development Commands

### Running the App
```bash
# Start development server
npm start

# Run on Android
npm run android

# Run on iOS
npm run ios

# Run on web
npm run web
```

### Environment Setup
- Copy `.env.example` to `.env` and fill in required values:
  - `EXPO_PUBLIC_SUPABASE_URL` - Supabase project URL
  - `EXPO_PUBLIC_SUPABASE_ANON_KEY` - Supabase anonymous key
  - `EXPO_PUBLIC_TUTORING_API_URL` - Backend API URL (defaults to http://localhost:8002)

## Architecture

### Frontend-Backend Separation
The frontend is a thin UI layer that:
- Handles user interface, navigation, and local state
- Calls backend APIs via typed service clients in `services/`
- **Does NOT contain tutoring logic, AI prompts, or teaching workflows**
- All AI orchestration happens in the backend (located at `../../app/`)

### Route Structure
This app uses Expo Router with file-based routing:

- `app/_layout.tsx` - Root layout with auth gate and deep link handler
- `app/(auth)/` - Authentication screens (login, signup, forgot-password, reset-password)
- `app/(tabs)/` - Main app tabs:
  - `index.tsx` - AI Tutor dashboard (primary screen)
  - `calculator.tsx` - Scientific calculator (TI-84 style)
  - `graph.tsx` - Graphing calculator
  - `saved.tsx` - Saved problems
  - `settings.tsx` - User settings and profile
- `app/edit-profile.tsx` - Edit user profile modal

### Authentication Flow
The app uses Supabase Auth with a comprehensive password recovery system:

1. **Auth Gate** (`app/_layout.tsx`): Controls access to screens based on auth state
   - Unauthenticated users → redirect to login
   - Authenticated users on auth screens → redirect to tabs
   - Special handling for password recovery flow

2. **Password Recovery**:
   - Web: Supabase auto-detects tokens in URL hash via `detectSessionInUrl: true`
   - Mobile: Deep links are manually parsed in `_layout.tsx` and tokens extracted from URL fragments
   - `isRecoveringPassword` flag prevents auth gate from redirecting users to tabs when they're mid-password-reset
   - After successful password reset, `clearPasswordRecovery()` allows normal navigation

3. **Deep Link Format**: `mathhelper://reset-password#access_token=...&refresh_token=...&type=recovery`

### State Management
Global state is managed via **AppContext** (`context/AppContext.tsx`):

- **Auth state**: `user`, `session`, `authLoading`, `isRecoveringPassword`
- **Saved items**: Problems solved and saved by the user (stored in Supabase)
- **Tutoring sessions**: Chat conversations with the AI tutor
- **Data migration**: On first login, migrates local AsyncStorage data to Supabase

### Service Layer (`services/`)
Each service module handles a specific domain:

- `agent.ts` - AI tutoring API calls (`/chat/start-session`, `/chat/message`, `/chat/close-session`)
- `api.ts` - Shared authenticated fetch helper (injects Supabase JWT tokens)
- `auth.ts` - Authentication operations (login, signup, signout, password reset)
- `database.ts` - Supabase database CRUD for saved items and sessions
- `storage.ts` - Supabase Storage operations for uploading/fetching images

### AI Tutoring Integration
The tutoring system works as follows:

1. **Session lifecycle**:
   - Call `startAgentSession()` to get a `session_id`
   - Send messages with `sendAgentMessage(sessionId, message, options)`
   - Close session with `closeAgentSession(sessionId)` to get summary and mastery updates

2. **Agent messages** support:
   - Text input
   - Base64-encoded images (for photo scanning)
   - Conversation history (for context)
   - Mode selection (explain, guide_me, hint, check_answer, or auto)

3. **Agent responses** include:
   - AI-generated response text
   - Detected topic and subject
   - Tools used by the backend
   - Graph data (for visualization)
   - Contextual suggestions for follow-up questions

### Image Handling
Images flow through this pipeline:
1. User selects photo via `ImagePicker` (camera or gallery)
2. Convert to base64 using `imageUriToBase64()` from `services/agent.ts`
3. Send to backend API with message
4. Backend processes with GPT-4o vision
5. Save to Supabase Storage using `uploadImage()` from `services/storage.ts`
6. Store storage path in database
7. Fetch signed URLs for display using `getImageUrl()`

### Component Architecture
Key reusable components in `components/`:

- `ResponseBubble.tsx` - Renders AI tutor responses with markdown, steps, and graphs
- `DesmosGraph.tsx` - Embeds Desmos graphing calculator for visualizations
- `MathRenderer.tsx` - Renders LaTeX math using KaTeX
- `StepCards.tsx` - Displays step-by-step solution cards
- `MessageReactions.tsx` - Helpful/confused reactions below AI messages
- `SuggestionChips.tsx` - Contextual follow-up question chips
- `ToolStatus.tsx` - Animated "thinking" indicator showing active tools

## Key Technical Patterns

### Platform-Specific Behavior
Use Platform.OS checks for web vs native differences:
```typescript
if (Platform.OS === 'web') {
  // Web-specific code
} else {
  // Native-specific code
}
```

Common cases:
- Supabase `detectSessionInUrl` (true on web, false on native)
- Deep link handling (browser URL vs Linking API)
- Confirmation dialogs (`window.confirm` vs `Alert.alert`)

### TypeScript Strictness
- `strict: true` is enabled in `tsconfig.json`
- Use proper types from `lib/database.types.ts` (auto-generated from Supabase schema)
- Service functions have explicit return types

### Styling Convention
- All styles use StyleSheet.create() at bottom of component files
- Color constants are defined in `constants/Colors.ts`
- Use `useSafeAreaInsets()` for platform-safe padding (notches, status bars)

### Error Handling
- API errors are caught and displayed to the user via error state
- Failed image uploads are logged but don't block the operation
- Network errors show retry buttons

## Backend API Connection

The backend is a Python FastAPI application located at `../../app/`. It provides:
- `/chat/start-session` - Initialize tutoring session
- `/chat/message` - Send message and get AI response
- `/chat/close-session` - Close session and get summary

All API calls require a Supabase JWT token in the `Authorization` header, which is automatically injected by `apiFetch()` in `services/api.ts`.

## Data Storage

### Supabase Tables
- `saved_items` - Saved math problems with solutions
- `tutoring_sessions` - Chat conversation history

### Supabase Storage Buckets
- User images are stored in storage buckets organized by user ID
- Signed URLs are generated for display (valid for limited time)

### Migration Strategy
- First-time users migrate local AsyncStorage data to Supabase automatically
- Migration runs once per user, marked with `@mathhelper_migrated_to_supabase` flag

## Important Notes

### Security
- Never expose `SUPABASE_SERVICE_ROLE_KEY` in the frontend
- Only use `SUPABASE_ANON_KEY` (row-level security enforces access control)
- All API calls to the backend require authenticated Supabase JWT tokens

### Calculator Tab
The calculator tab (`app/(tabs)/calculator.tsx`) is a full TI-84-style scientific calculator with white/purple theme. It's completely self-contained and doesn't interact with the AI backend.

### Testing Locally
1. Start the backend: `cd ../../app && python main.py` (runs on port 8002)
2. Start Expo: `npm start` in this directory
3. Ensure `.env` has correct `EXPO_PUBLIC_TUTORING_API_URL` pointing to localhost

### Common Gotchas
- Image URIs from ImagePicker expire - always upload to Supabase Storage before saving
- Deep links require URL fragments (`#access_token=...`) not query params (`?access_token=...`)
- Password recovery sessions are valid sessions - use `isRecoveringPassword` flag to handle properly
- AsyncStorage only works in client environment - check `typeof window !== 'undefined'` before using
