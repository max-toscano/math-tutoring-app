/**
 * MathRenderer.tsx
 * Renders AI tutor responses with KaTeX math and inline graph images.
 *
 * Web: Uses an iframe with KaTeX loaded (WebView doesn't work on web)
 * Native (iOS/Android): Uses react-native-webview
 */

import { useState, useEffect, useRef } from 'react';
import { View, Platform } from 'react-native';
import { Colors } from '../constants/Colors';

interface GraphOutput {
  graph_type?: string;
  image_base64?: string;
}

interface MathRendererProps {
  content: string;
  graphs?: GraphOutput[];
  isUser?: boolean;
}

function buildHtml(content: string, graphs: GraphOutput[], textColor: string): string {
  const graphsHtml = graphs
    .filter((g) => g.image_base64)
    .map(
      (g) =>
        `<div class="graph">
          <img src="data:image/png;base64,${g.image_base64}" />
        </div>`,
    )
    .join('');

  // Preserve $$ display blocks as-is, only escape HTML outside of math
  // Step 1: Pull out all math blocks, escape the rest, put them back
  const mathBlocks: string[] = [];
  const placeholder = '___MATH_BLOCK___';

  // Extract $$...$$ and $...$ blocks before escaping
  let processed = content;

  // Extract display math: $$...$$ and \[...\]
  processed = processed.replace(/\$\$([\s\S]*?)\$\$/g, (match) => {
    mathBlocks.push(match);
    return placeholder;
  });
  processed = processed.replace(/\\\[([\s\S]*?)\\\]/g, (match) => {
    mathBlocks.push(match);
    return placeholder;
  });

  // Extract inline math: $...$ and \(...\)
  processed = processed.replace(/\$([^\$\n]+?)\$/g, (match) => {
    mathBlocks.push(match);
    return placeholder;
  });
  processed = processed.replace(/\\\(([\s\S]*?)\\\)/g, (match) => {
    mathBlocks.push(match);
    return placeholder;
  });

  // Now escape HTML in the non-math text
  processed = processed
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br/>');

  // Put math blocks back (unescaped)
  let blockIndex = 0;
  const escapedContent = processed.replace(new RegExp(placeholder, 'g'), () => {
    return mathBlocks[blockIndex++] || '';
  });

  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
      <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          font-size: 15px;
          line-height: 1.6;
          color: ${textColor};
          background: transparent;
          padding: 0;
          overflow: visible;
        }
        .content { word-wrap: break-word; }
        .katex { font-size: 1.05em; }
        .katex-display {
          margin: 12px 0;
          padding: 12px 16px;
          background: #F0EDFF;
          border-left: 4px solid #6C63FF;
          border-radius: 8px;
          overflow-x: auto;
          overflow-y: hidden;
        }
        .graph { margin: 12px 0; border-radius: 12px; overflow: hidden; }
        .graph img { width: 100%; height: auto; display: block; border-radius: 12px; }
      </style>
    </head>
    <body>
      <div class="content" id="content">${escapedContent}</div>
      ${graphsHtml}
      <script>
        document.addEventListener("DOMContentLoaded", function() {
          renderMathInElement(document.getElementById("content"), {
            delimiters: [
              { left: "$$", right: "$$", display: true },
              { left: "$", right: "$", display: false },
              { left: "\\\\[", right: "\\\\]", display: true },
              { left: "\\\\(", right: "\\\\)", display: false }
            ],
            throwOnError: false
          });
          // Send height multiple times as KaTeX may still be rendering
          function sendHeight() {
            var h = document.body.scrollHeight;
            window.parent.postMessage({ type: 'mathHeight', height: h, id: '${Date.now()}' }, '*');
            if (window.ReactNativeWebView) {
              window.ReactNativeWebView.postMessage(JSON.stringify({ height: h }));
            }
          }
          setTimeout(sendHeight, 100);
          setTimeout(sendHeight, 500);
          setTimeout(sendHeight, 1000);
          setTimeout(sendHeight, 2000);
        });
      </script>
    </body>
    </html>
  `;
}

export default function MathRenderer({ content, graphs, isUser }: MathRendererProps) {
  if (Platform.OS === 'web') {
    return <MathRendererWeb content={content} graphs={graphs} isUser={isUser} />;
  }
  return <MathRendererNative content={content} graphs={graphs} isUser={isUser} />;
}

// ── Web: iframe ──────────────────────────────────────────────────────────
function MathRendererWeb({ content, graphs, isUser }: MathRendererProps) {
  // Estimate initial height from content length (rough: 1 line per 60 chars + padding)
  const lineCount = Math.ceil(content.length / 60) + (content.match(/\$\$/g)?.length ?? 0) * 2;
  const estimatedHeight = Math.max(40, lineCount * 24 + 20);
  const [height, setHeight] = useState(estimatedHeight);
  const iframeId = useRef(`math_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`).current;
  const textColor = isUser ? '#FFFFFF' : (Colors.text || '#1A1A2E');
  const html = buildHtml(content, graphs ?? [], textColor);

  useEffect(() => {
    function handleMessage(event: MessageEvent) {
      if (event.data?.type === 'mathHeight' && event.data?.height > 0) {
        // Take the reported height directly (last measurement wins)
        setHeight(event.data.height + 8);
      }
    }
    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  return (
    <View>
      {/* @ts-ignore — iframe works on web */}
      <iframe
        srcDoc={html}
        style={{
          width: '100%',
          height: height,
          border: 'none',
          background: 'transparent',
          display: 'block',
        }}
      />
    </View>
  );
}

// ── Native: WebView ──────────────────────────────────────────────────────
function MathRendererNative({ content, graphs, isUser }: MathRendererProps) {
  const [height, setHeight] = useState(80);
  const textColor = isUser ? '#FFFFFF' : (Colors.text || '#1A1A2E');
  const html = buildHtml(content, graphs ?? [], textColor);

  let WebView: any;
  try {
    WebView = require('react-native-webview').default;
  } catch {
    // Fallback if WebView not available
    const { Text } = require('react-native');
    return <Text style={{ color: textColor, fontSize: 15, lineHeight: 22 }}>{content}</Text>;
  }

  return (
    <View style={{ minHeight: height, width: '100%' }}>
      <WebView
        source={{ html }}
        style={{ height, width: '100%', backgroundColor: 'transparent', opacity: 0.99 }}
        scrollEnabled={false}
        showsVerticalScrollIndicator={false}
        originWhitelist={['*']}
        javaScriptEnabled={true}
        onMessage={(event: any) => {
          try {
            const data = JSON.parse(event.nativeEvent.data);
            if (data.height > 0) setHeight(data.height + 16);
          } catch {}
        }}
      />
    </View>
  );
}
