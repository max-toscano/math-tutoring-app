import { Amplify } from 'aws-amplify';

const COGNITO_USER_POOL_ID = process.env.EXPO_PUBLIC_COGNITO_USER_POOL_ID;
const COGNITO_CLIENT_ID = process.env.EXPO_PUBLIC_COGNITO_CLIENT_ID;

if (!COGNITO_USER_POOL_ID || !COGNITO_CLIENT_ID) {
  throw new Error('Missing Cognito environment variables. Add them to your .env file.');
}

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: COGNITO_USER_POOL_ID,
      userPoolClientId: COGNITO_CLIENT_ID,
    },
  },
});
