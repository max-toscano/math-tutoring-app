/**
 * YouTubePlayer.tsx
 * Reusable YouTube video player component.
 *
 * Works on both web (iframe) and native (WebView).
 * No YouTube API key needed — uses the standard embed URL.
 *
 * Features:
 *  - Responsive sizing
 *  - Optional title and channel display
 *  - Callback when video ends (to auto-advance to review)
 */

import { View, Text, StyleSheet, Platform } from 'react-native';
import { Colors } from '../constants/Colors';

interface YouTubePlayerProps {
  videoId: string;
  title?: string;
  channel?: string;
  height?: number;
}

function buildEmbedUrl(videoId: string): string {
  return `https://www.youtube.com/embed/${videoId}?rel=0&modestbranding=1&playsinline=1`;
}

function buildEmbedHtml(videoId: string): string {
  return `<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { margin: 0; padding: 0; }
    html, body { width: 100%; height: 100%; background: #000; }
    iframe { width: 100%; height: 100%; border: none; }
  </style>
</head>
<body>
  <iframe
    src="${buildEmbedUrl(videoId)}"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen
  ></iframe>
</body>
</html>`;
}

export default function YouTubePlayer({ videoId, title, channel, height = 220 }: YouTubePlayerProps) {
  return (
    <View style={styles.container}>
      <View style={[styles.playerWrap, { height }]}>
        <PlayerView videoId={videoId} height={height} />
      </View>
      {(title || channel) && (
        <View style={styles.info}>
          {title && <Text style={styles.title} numberOfLines={2}>{title}</Text>}
          {channel && <Text style={styles.channel}>{channel}</Text>}
        </View>
      )}
    </View>
  );
}

function PlayerView({ videoId, height }: { videoId: string; height: number }) {
  if (Platform.OS === 'web') {
    return (
      // @ts-ignore
      <iframe
        src={buildEmbedUrl(videoId)}
        style={{
          width: '100%',
          height: height,
          border: 'none',
          borderRadius: 12,
        }}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      />
    );
  }

  let WebView: any;
  try {
    WebView = require('react-native-webview').default;
  } catch {
    return <Text style={styles.fallback}>Video player requires WebView</Text>;
  }

  return (
    <WebView
      source={{ html: buildEmbedHtml(videoId) }}
      style={{ width: '100%', height, borderRadius: 12 }}
      javaScriptEnabled={true}
      domStorageEnabled={true}
      allowsInlineMediaPlayback={true}
      mediaPlaybackRequiresUserAction={false}
      originWhitelist={['*']}
      mixedContentMode="always"
    />
  );
}

const styles = StyleSheet.create({
  container: {
    borderRadius: 14,
    overflow: 'hidden',
    backgroundColor: '#000',
  },
  playerWrap: {
    width: '100%',
    borderRadius: 12,
    overflow: 'hidden',
  },
  info: {
    padding: 12,
    backgroundColor: Colors.card || '#FFF',
  },
  title: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.text || '#1A1A2E',
    lineHeight: 20,
  },
  channel: {
    fontSize: 12,
    color: Colors.textMuted || '#999',
    marginTop: 2,
  },
  fallback: {
    padding: 20,
    color: '#999',
    textAlign: 'center',
  },
});
