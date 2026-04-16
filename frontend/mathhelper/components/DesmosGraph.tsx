/**
 * DesmosGraph.tsx
 * Renders an interactive Desmos calculator graph.
 *
 * Web: uses an iframe loading the Desmos API
 * Native: uses react-native-webview loading the Desmos API
 */

import { useState, useCallback } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Platform, Modal } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/Colors';

interface DesmosExpression {
  latex: string;
  color?: string;
  lineStyle?: string;
  label?: string;
  fillOpacity?: number;
  pointStyle?: string;
}

interface DesmosBounds {
  left: number;
  right: number;
  top: number;
  bottom: number;
}

interface DesmosGraphProps {
  expressions: DesmosExpression[];
  bounds?: DesmosBounds;
  graphType?: string;
}

function buildDesmosHtml(expressions: DesmosExpression[], bounds?: DesmosBounds): string {
  // Get API key — hardcode fallback for reliability
  const apiKey = process.env.EXPO_PUBLIC_DESMOS_API_KEY || '8cc7d279bb714ca5b8cb90afbf370a8b';

  // Build expression setup JS
  const exprLines = expressions.map((expr, i) => {
    // Escape the latex for embedding in a JS string
    const safeLatex = expr.latex
      .replace(/\\/g, '\\\\')  // escape backslashes for JS string
      .replace(/'/g, "\\'");    // escape single quotes

    const parts = [`id: 'expr${i}'`, `latex: '${safeLatex}'`];
    if (expr.color) parts.push(`color: '${expr.color}'`);
    if (expr.lineStyle === 'DASHED') parts.push(`lineStyle: Desmos.Styles.DASHED`);
    if (expr.fillOpacity != null) parts.push(`fillOpacity: ${expr.fillOpacity}`);
    if (expr.pointStyle === 'POINT') parts.push(`pointSize: 12`);

    return `calculator.setExpression({ ${parts.join(', ')} });`;
  }).join('\n        ');

  const boundsJs = bounds
    ? `calculator.setMathBounds({ left: ${bounds.left}, right: ${bounds.right}, top: ${bounds.top}, bottom: ${bounds.bottom} });`
    : '';

  return `<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <script src="https://www.desmos.com/api/v1.9/calculator.js?apiKey=${apiKey}"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 100%; height: 100%; overflow: hidden; background: #fff; }
    #calculator { width: 100%; height: 100%; }
    #error { display: none; padding: 20px; color: red; font-family: sans-serif; }
  </style>
</head>
<body>
  <div id="calculator"></div>
  <div id="error"></div>
  <script>
    function reportError(msg) {
      document.getElementById('error').style.display = 'block';
      document.getElementById('error').textContent = msg;
      if (window.ReactNativeWebView) {
        window.ReactNativeWebView.postMessage(JSON.stringify({ type: 'error', message: msg }));
      }
    }

    try {
      if (typeof Desmos === 'undefined') throw new Error('Desmos failed to load — check network connection.');
      var elt = document.getElementById('calculator');
      var calculator = Desmos.GraphingCalculator(elt, {
        expressionsCollapsed: true,
        settingsMenu: false,
        zoomButtons: true,
        lockViewport: false,
        border: false,
        keypad: false,
      });

      ${exprLines}
      ${boundsJs}
    } catch(e) {
      reportError('Graph error: ' + e.message);
    }
  </script>
</body>
</html>`;
}

export default function DesmosGraph({ expressions, bounds, graphType }: DesmosGraphProps) {
  const [fullScreen, setFullScreen] = useState(false);
  const [graphError, setGraphError] = useState<string | null>(null);
  const html = buildDesmosHtml(expressions, bounds);

  const handleGraphError = useCallback((msg: string) => {
    setGraphError(msg);
  }, []);

  return (
    <View style={styles.container}>
      <View style={styles.graphCard}>
        {graphError ? (
          <View style={styles.errorContainer}>
            <Ionicons name="warning-outline" size={24} color="#E57373" />
            <Text style={styles.errorText}>Could not render graph</Text>
            <Text style={styles.errorSubtext}>{graphError}</Text>
          </View>
        ) : (
          <GraphView html={html} height={280} onError={handleGraphError} />
        )}
        <View style={styles.footer}>
          <View style={styles.footerLeft}>
            <Ionicons name="analytics-outline" size={14} color="#999" />
            <Text style={styles.footerText}>
              {graphType?.replace(/_/g, ' ') || 'Interactive Graph'}
            </Text>
            <Text style={styles.exprPreview} numberOfLines={1}>
              {expressions[0]?.latex || ''}
            </Text>
          </View>
          <TouchableOpacity
            style={styles.expandBtn}
            onPress={() => setFullScreen(true)}
            activeOpacity={0.7}
          >
            <Ionicons name="expand-outline" size={16} color={Colors.primary} />
            <Text style={styles.expandText}>Full Screen</Text>
          </TouchableOpacity>
        </View>
      </View>

      <Modal visible={fullScreen} animationType="slide">
        <View style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>
              {expressions[0]?.latex || 'Graph'}
            </Text>
            <TouchableOpacity
              style={styles.modalClose}
              onPress={() => setFullScreen(false)}
              activeOpacity={0.7}
            >
              <Ionicons name="close" size={24} color={Colors.text || '#333'} />
            </TouchableOpacity>
          </View>
          <GraphView html={html} height="100%" onError={handleGraphError} />
        </View>
      </Modal>
    </View>
  );
}

function GraphView({
  html,
  height,
  onError,
}: {
  html: string;
  height: number | string;
  onError?: (msg: string) => void;
}) {
  if (Platform.OS === 'web') {
    return (
      // @ts-ignore
      <iframe
        srcDoc={html}
        style={{
          width: '100%',
          height: typeof height === 'number' ? height : '100%',
          border: 'none',
          borderRadius: 12,
          background: '#fff',
        }}
        allow="accelerometer"
      />
    );
  }

  let WebView: any;
  try {
    WebView = require('react-native-webview').default;
  } catch {
    return <Text style={{ padding: 20, color: '#999' }}>Graph requires WebView</Text>;
  }

  return (
    <WebView
      source={{ html }}
      style={{
        width: '100%',
        height: typeof height === 'number' ? height : undefined,
        flex: typeof height === 'string' ? 1 : undefined,
        borderRadius: 12,
        backgroundColor: '#fff',
      }}
      javaScriptEnabled={true}
      domStorageEnabled={true}
      originWhitelist={['*']}
      scrollEnabled={false}
      mixedContentMode="always"
      onError={() => onError?.('WebView failed to load.')}
      onMessage={(event: any) => {
        try {
          const data = JSON.parse(event.nativeEvent.data);
          if (data.type === 'error') onError?.(data.message);
        } catch {}
      }}
    />
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8,
  },
  graphCard: {
    borderRadius: 14,
    overflow: 'hidden',
    backgroundColor: '#FFF',
    borderWidth: 1,
    borderColor: '#E8E8F0',
  },
  footer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderTopWidth: 1,
    borderTopColor: '#E8E8F0',
  },
  footerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    flex: 1,
  },
  footerText: {
    fontSize: 12,
    color: '#999',
    textTransform: 'capitalize',
  },
  exprPreview: {
    fontSize: 11,
    color: Colors.primary,
    fontStyle: 'italic',
    marginLeft: 4,
    flex: 1,
  },
  expandBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
    backgroundColor: Colors.primaryLight || '#EDE9FF',
  },
  expandText: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.primary,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: '#FFF',
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingTop: 50,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#E8E8F0',
  },
  modalTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text || '#333',
    flex: 1,
  },
  modalClose: {
    padding: 4,
  },
  errorContainer: {
    height: 280,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingHorizontal: 20,
    backgroundColor: '#FFF8F8',
  },
  errorText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#C62828',
  },
  errorSubtext: {
    fontSize: 12,
    color: '#999',
    textAlign: 'center',
  },
});
