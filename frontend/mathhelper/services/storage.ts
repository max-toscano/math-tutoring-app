/**
 * Storage service — uploads images to Supabase Storage.
 *
 * Files are stored under: math-images/{userId}/{timestamp}.{ext}
 * RLS policies enforce the userId folder constraint.
 */
import { Platform } from 'react-native';
import { supabase } from '../lib/supabase';

const BUCKET = 'math-images';

/**
 * Upload a local image URI to Supabase Storage.
 * Returns the storage path (not the full URL — use getImageUrl to get a signed URL).
 */
export async function uploadImage(
  userId: string,
  localUri: string,
): Promise<string> {
  const ext = localUri.split('.').pop()?.split('?')[0] ?? 'jpg';
  const fileName = `${userId}/${Date.now()}_${Math.random().toString(36).slice(2)}.${ext}`;

  let fileBody: Blob | ArrayBuffer;
  let contentType = ext === 'png' ? 'image/png' : 'image/jpeg';

  if (Platform.OS === 'web') {
    const res = await fetch(localUri);
    fileBody = await res.blob();
    contentType = (fileBody as Blob).type || contentType;
  } else {
    // React Native: read as base64, convert to ArrayBuffer
    const FS = await import('expo-file-system');
    const base64 = await FS.readAsStringAsync(localUri, {
      encoding: FS.EncodingType.Base64,
    });
    // Decode base64 to binary
    const binaryString = atob(base64);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    fileBody = bytes.buffer as ArrayBuffer;
  }

  const { error } = await supabase.storage
    .from(BUCKET)
    .upload(fileName, fileBody, {
      contentType,
      upsert: false,
    });

  if (error) throw error;
  return fileName;
}

/**
 * Get a signed URL for an image in storage (valid for 1 hour).
 */
export async function getImageUrl(storagePath: string): Promise<string> {
  const { data, error } = await supabase.storage
    .from(BUCKET)
    .createSignedUrl(storagePath, 3600); // 1 hour

  if (error) throw error;
  return data.signedUrl;
}

/**
 * Delete an image from storage.
 */
export async function deleteImage(storagePath: string): Promise<void> {
  const { error } = await supabase.storage.from(BUCKET).remove([storagePath]);
  if (error) throw error;
}
