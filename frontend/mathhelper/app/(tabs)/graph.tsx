/**
 * graph.tsx
 * TI-84 Style Graphing Calculator — Desmos-powered, zero AI.
 *
 * Split screen:
 *  - Top ~55%: Desmos interactive graph
 *  - Bottom ~45%: TI-84 style keypad + function editor
 *
 * Modes (like a real TI-84):
 *  - Y=     : edit function expressions (Y1, Y2, Y3...)
 *  - GRAPH  : view the graph with all active functions
 *  - TABLE  : see x/y value table for active functions
 *
 * No AI. User → keypad → Desmos. Instant.
 */

import { useState, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  Platform,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

const DESMOS_API_KEY = process.env.EXPO_PUBLIC_DESMOS_API_KEY || '8cc7d279bb714ca5b8cb90afbf370a8b';
const SCREEN_WIDTH = Dimensions.get('window').width;

// ── Colors (white + purple theme — matches app) ─────────────────────────
const TI = {
  bg: '#F0F2F5',
  bgLight: '#FFFFFF',
  bgKey: '#FFFFFF',
  bgKeyBlue: '#6C63FF',
  bgKeyGreen: '#4ECDC4',
  bgKeyOrange: '#FF9F43',
  bgKeyRed: '#FF6B6B',
  bgKey2nd: '#6C63FF',
  text: '#1A1A2E',
  textDim: '#6B7280',
  accent: '#6C63FF',
  green: '#4ECDC4',
  blue: '#6C63FF',
  orange: '#FF9F43',
  red: '#FF6B6B',
  funcColors: ['#6C63FF', '#FF6B6B', '#4ECDC4', '#FF9F43', '#2ECC71', '#9B59B6', '#E74C3C'],
  border: '#E5E7EB',
  display: '#FFFFFF',
};

// ── Types ────────────────────────────────────────────────────────────────
interface FuncEntry {
  id: string;
  label: string;
  expr: string;
  active: boolean;
  color: string;
}

type Mode = 'graph' | 'yedit' | 'table';

// ── Main Component ───────────────────────────────────────────────────────
export default function GraphingCalculatorScreen() {
  const insets = useSafeAreaInsets();

  const [mode, setMode] = useState<Mode>('yedit');
  const [functions, setFunctions] = useState<FuncEntry[]>([
    { id: 'Y1', label: 'Y₁', expr: '', active: true, color: TI.funcColors[0] },
    { id: 'Y2', label: 'Y₂', expr: '', active: true, color: TI.funcColors[1] },
    { id: 'Y3', label: 'Y₃', expr: '', active: true, color: TI.funcColors[2] },
    { id: 'Y4', label: 'Y₄', expr: '', active: true, color: TI.funcColors[3] },
  ]);
  const [activeFunc, setActiveFunc] = useState('Y1');
  const [is2nd, setIs2nd] = useState(false);
  const [cursorPos, setCursorPos] = useState(0);

  // Get the currently selected function
  const currentFunc = functions.find((f) => f.id === activeFunc);
  const currentExpr = currentFunc?.expr ?? '';

  // ── Expression editing ───────────────────────────────────────────────
  function insertAtCursor(text: string) {
    setFunctions((prev) =>
      prev.map((f) => {
        if (f.id !== activeFunc) return f;
        const before = f.expr.slice(0, cursorPos);
        const after = f.expr.slice(cursorPos);
        return { ...f, expr: before + text + after };
      })
    );
    setCursorPos((p) => p + text.length);
  }

  function handleBackspace() {
    if (cursorPos <= 0) return;
    setFunctions((prev) =>
      prev.map((f) => {
        if (f.id !== activeFunc) return f;
        const before = f.expr.slice(0, cursorPos - 1);
        const after = f.expr.slice(cursorPos);
        return { ...f, expr: before + after };
      })
    );
    setCursorPos((p) => Math.max(0, p - 1));
  }

  function handleClear() {
    setFunctions((prev) =>
      prev.map((f) => (f.id === activeFunc ? { ...f, expr: '' } : f))
    );
    setCursorPos(0);
  }

  function toggleFuncActive(id: string) {
    setFunctions((prev) =>
      prev.map((f) => (f.id === id ? { ...f, active: !f.active } : f))
    );
  }

  function handleGraph() {
    setMode('graph');
  }

  // Build Desmos expressions from active functions
  const desmosExpressions = functions
    .filter((f) => f.active && f.expr.trim())
    .map((f) => ({
      id: f.id,
      latex: `y = ${formatForDesmos(f.expr)}`,
      color: f.color,
    }));

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      {/* ── Top: Mode Bar ── */}
      <View style={styles.modeBar}>
        <ModeButton label="Y=" active={mode === 'yedit'} onPress={() => setMode('yedit')} />
        <ModeButton
          label="GRAPH"
          active={mode === 'graph'}
          onPress={handleGraph}
          highlight={desmosExpressions.length > 0}
        />
        <ModeButton label="TABLE" active={mode === 'table'} onPress={() => setMode('table')} />
        <View style={{ flex: 1 }} />
        <TouchableOpacity
          style={styles.mode2ndBtn}
          onPress={() => setIs2nd((p) => !p)}
          activeOpacity={0.7}
        >
          <Text style={[styles.mode2ndText, is2nd && styles.mode2ndActive]}>2nd</Text>
        </TouchableOpacity>
      </View>

      {/* ── Middle: Graph / Y= Editor / Table ── */}
      <View style={styles.screenArea}>
        {mode === 'graph' && (
          <DesmosView expressions={desmosExpressions} />
        )}
        {mode === 'yedit' && (
          <YEditScreen
            functions={functions}
            activeFunc={activeFunc}
            cursorPos={cursorPos}
            onSelectFunc={(id) => {
              setActiveFunc(id);
              setCursorPos(functions.find((f) => f.id === id)?.expr.length ?? 0);
            }}
            onToggleActive={toggleFuncActive}
          />
        )}
        {mode === 'table' && (
          <TableScreen functions={functions} />
        )}
      </View>

      {/* ── Bottom: Keypad ── */}
      <View style={[styles.keypad, { paddingBottom: Math.max(insets.bottom, 4) }]}>
        {/* Row 1: Trig / Special */}
        <View style={styles.keyRow}>
          <CalcKey label={is2nd ? 'sin⁻¹' : 'sin'} onPress={() => insertAtCursor(is2nd ? 'arcsin(' : 'sin(')} color={TI.bgKeyBlue} />
          <CalcKey label={is2nd ? 'cos⁻¹' : 'cos'} onPress={() => insertAtCursor(is2nd ? 'arccos(' : 'cos(')} color={TI.bgKeyBlue} />
          <CalcKey label={is2nd ? 'tan⁻¹' : 'tan'} onPress={() => insertAtCursor(is2nd ? 'arctan(' : 'tan(')} color={TI.bgKeyBlue} />
          <CalcKey label="π" onPress={() => insertAtCursor('π')} color={TI.bgKeyBlue} />
          <CalcKey label="^" onPress={() => insertAtCursor('^')} color={TI.bgKeyBlue} />
        </View>

        {/* Row 2: Functions */}
        <View style={styles.keyRow}>
          <CalcKey label={is2nd ? 'eˣ' : 'ln'} onPress={() => insertAtCursor(is2nd ? 'e^(' : 'ln(')} color={TI.bgKeyBlue} />
          <CalcKey label={is2nd ? '10ˣ' : 'log'} onPress={() => insertAtCursor(is2nd ? '10^(' : 'log(')} color={TI.bgKeyBlue} />
          <CalcKey label="√" onPress={() => insertAtCursor('√(')} color={TI.bgKeyBlue} />
          <CalcKey label="x²" onPress={() => insertAtCursor('^2')} color={TI.bgKeyBlue} />
          <CalcKey label="|x|" onPress={() => insertAtCursor('|')} color={TI.bgKeyBlue} />
        </View>

        {/* Row 3: Variables + parens */}
        <View style={styles.keyRow}>
          <CalcKey label="x" onPress={() => insertAtCursor('x')} color={TI.bgKeyGreen} wide />
          <CalcKey label="(" onPress={() => insertAtCursor('(')} color={TI.bgKey} />
          <CalcKey label=")" onPress={() => insertAtCursor(')')} color={TI.bgKey} />
          <CalcKey label="," onPress={() => insertAtCursor(',')} color={TI.bgKey} />
          <CalcKey label="DEL" onPress={handleBackspace} color={TI.bgKeyRed} icon="backspace-outline" />
        </View>

        {/* Row 4-6: Numbers + Operators */}
        <View style={styles.keyRow}>
          <CalcKey label="7" onPress={() => insertAtCursor('7')} />
          <CalcKey label="8" onPress={() => insertAtCursor('8')} />
          <CalcKey label="9" onPress={() => insertAtCursor('9')} />
          <CalcKey label="÷" onPress={() => insertAtCursor('/')} color={TI.bgKeyOrange} />
          <CalcKey label="CLR" onPress={handleClear} color={TI.bgKeyRed} small />
        </View>

        <View style={styles.keyRow}>
          <CalcKey label="4" onPress={() => insertAtCursor('4')} />
          <CalcKey label="5" onPress={() => insertAtCursor('5')} />
          <CalcKey label="6" onPress={() => insertAtCursor('6')} />
          <CalcKey label="×" onPress={() => insertAtCursor('*')} color={TI.bgKeyOrange} />
          <CalcKey label="Y=" onPress={() => setMode('yedit')} color={TI.bgKeyGreen} small />
        </View>

        <View style={styles.keyRow}>
          <CalcKey label="1" onPress={() => insertAtCursor('1')} />
          <CalcKey label="2" onPress={() => insertAtCursor('2')} />
          <CalcKey label="3" onPress={() => insertAtCursor('3')} />
          <CalcKey label="−" onPress={() => insertAtCursor('-')} color={TI.bgKeyOrange} />
          <CalcKey label="GRAPH" onPress={handleGraph} color={TI.accent} small />
        </View>

        <View style={styles.keyRow}>
          <CalcKey label="0" onPress={() => insertAtCursor('0')} wide />
          <CalcKey label="." onPress={() => insertAtCursor('.')} />
          <CalcKey label="(−)" onPress={() => insertAtCursor('-')} />
          <CalcKey label="+" onPress={() => insertAtCursor('+')} color={TI.bgKeyOrange} />
        </View>
      </View>
    </View>
  );
}

// ── Y= Editor Screen ─────────────────────────────────────────────────────

function YEditScreen({
  functions,
  activeFunc,
  cursorPos,
  onSelectFunc,
  onToggleActive,
}: {
  functions: FuncEntry[];
  activeFunc: string;
  cursorPos: number;
  onSelectFunc: (id: string) => void;
  onToggleActive: (id: string) => void;
}) {
  return (
    <View style={styles.yEditContainer}>
      <Text style={styles.yEditTitle}>Plot Functions</Text>
      {functions.map((f) => {
        const isActive = f.id === activeFunc;
        return (
          <TouchableOpacity
            key={f.id}
            style={[styles.yEditRow, isActive && styles.yEditRowActive]}
            onPress={() => onSelectFunc(f.id)}
            activeOpacity={0.7}
          >
            {/* Toggle visibility */}
            <TouchableOpacity onPress={() => onToggleActive(f.id)} style={styles.yEditToggle}>
              <View style={[styles.yEditDot, { backgroundColor: f.active ? f.color : '#555' }]}>
                {f.active && <Ionicons name="checkmark" size={10} color="#FFF" />}
              </View>
            </TouchableOpacity>

            {/* Label */}
            <Text style={[styles.yEditLabel, { color: f.color }]}>{f.label} =</Text>

            {/* Expression display */}
            <View style={styles.yEditExprWrap}>
              <Text style={[styles.yEditExpr, !f.expr && styles.yEditExprPlaceholder]}>
                {f.expr || 'enter expression'}
              </Text>
              {isActive && (
                <View style={styles.yEditCursor} />
              )}
            </View>
          </TouchableOpacity>
        );
      })}
      <Text style={styles.yEditHint}>
        Select a row, then use the keypad to enter your function.{'\n'}
        Press GRAPH to plot.
      </Text>
    </View>
  );
}

// ── Table Screen ─────────────────────────────────────────────────────────

function TableScreen({ functions }: { functions: FuncEntry[] }) {
  const activeExprs = functions.filter((f) => f.active && f.expr.trim());

  // Generate simple x values
  const xValues = Array.from({ length: 13 }, (_, i) => i - 6);

  return (
    <ScrollView style={styles.tableContainer}>
      <View style={styles.tableHeader}>
        <Text style={[styles.tableCell, styles.tableCellHeader, { flex: 0.8 }]}>X</Text>
        {activeExprs.map((f) => (
          <Text key={f.id} style={[styles.tableCell, styles.tableCellHeader, { color: f.color }]}>
            {f.label}
          </Text>
        ))}
      </View>
      {xValues.map((x) => (
        <View key={x} style={styles.tableRow}>
          <Text style={[styles.tableCell, { flex: 0.8 }]}>{x}</Text>
          {activeExprs.map((f) => (
            <Text key={f.id} style={styles.tableCell}>
              {evaluateSimple(f.expr, x)}
            </Text>
          ))}
        </View>
      ))}
    </ScrollView>
  );
}

// ── Desmos Graph View ────────────────────────────────────────────────────

function DesmosView({ expressions }: { expressions: { id: string; latex: string; color: string }[] }) {
  const exprSetup = expressions
    .map((e) => {
      const safeLatex = e.latex.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
      return `calculator.setExpression({ id: '${e.id}', latex: '${safeLatex}', color: '${e.color}' });`;
    })
    .join('\n      ');

  const html = `<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <script src="https://www.desmos.com/api/v1.9/calculator.js?apiKey=${DESMOS_API_KEY}"></script>
  <style>
    * { margin: 0; padding: 0; }
    html, body { width: 100%; height: 100%; overflow: hidden; background: #FFFFFF; }
    #calculator { width: 100%; height: 100%; }
  </style>
</head>
<body>
  <div id="calculator"></div>
  <script>
    var elt = document.getElementById('calculator');
    var calculator = Desmos.GraphingCalculator(elt, {
      expressionsCollapsed: true,
      settingsMenu: false,
      zoomButtons: true,
      lockViewport: false,
      border: false,
      keypad: false,
      invertedColors: false,
    });
    ${exprSetup}
  </script>
</body>
</html>`;

  if (expressions.length === 0) {
    return (
      <View style={styles.emptyGraph}>
        <Ionicons name="analytics-outline" size={40} color="#444" />
        <Text style={styles.emptyGraphText}>Enter functions in Y= then press GRAPH</Text>
      </View>
    );
  }

  if (Platform.OS === 'web') {
    return (
      // @ts-ignore
      <iframe srcDoc={html} style={{ width: '100%', height: '100%', border: 'none' }} allow="accelerometer" />
    );
  }

  let WebView: any;
  try { WebView = require('react-native-webview').default; } catch {
    return <Text style={{ padding: 20, color: '#999' }}>WebView required</Text>;
  }
  return (
    <WebView
      source={{ html }}
      style={{ width: '100%', height: '100%' }}
      javaScriptEnabled domStorageEnabled
      originWhitelist={['*']}
      scrollEnabled={false}
      mixedContentMode="always"
    />
  );
}

// ── Calculator Key ───────────────────────────────────────────────────────

function CalcKey({
  label, onPress, color, icon, wide, small,
}: {
  label: string; onPress: () => void; color?: string; icon?: string; wide?: boolean; small?: boolean;
}) {
  const isColored = color && color !== TI.bgKey;
  const textColor = isColored ? '#FFFFFF' : TI.text;

  return (
    <TouchableOpacity
      style={[
        styles.key,
        { backgroundColor: color || TI.bgKey },
        isColored && { borderColor: color },
        wide && styles.keyWide,
      ]}
      onPress={onPress}
      activeOpacity={0.6}
    >
      {icon ? (
        <Ionicons name={icon as any} size={18} color={textColor} />
      ) : (
        <Text style={[styles.keyText, small && styles.keyTextSmall, { color: textColor }]}>{label}</Text>
      )}
    </TouchableOpacity>
  );
}

// ── Mode Button ──────────────────────────────────────────────────────────

function ModeButton({
  label, active, onPress, highlight,
}: {
  label: string; active: boolean; onPress: () => void; highlight?: boolean;
}) {
  return (
    <TouchableOpacity
      style={[styles.modeBtn, active && styles.modeBtnActive, highlight && !active && styles.modeBtnHighlight]}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <Text style={[styles.modeBtnText, active && styles.modeBtnTextActive]}>{label}</Text>
    </TouchableOpacity>
  );
}

// ── Helpers ──────────────────────────────────────────────────────────────

function formatForDesmos(expr: string): string {
  return expr
    .replace(/\bsin\(/gi, '\\sin(')
    .replace(/\bcos\(/gi, '\\cos(')
    .replace(/\btan\(/gi, '\\tan(')
    .replace(/\bcsc\(/gi, '\\csc(')
    .replace(/\bsec\(/gi, '\\sec(')
    .replace(/\bcot\(/gi, '\\cot(')
    .replace(/\barcsin\(/gi, '\\arcsin(')
    .replace(/\barccos\(/gi, '\\arccos(')
    .replace(/\barctan\(/gi, '\\arctan(')
    .replace(/\bln\(/gi, '\\ln(')
    .replace(/\blog\(/gi, '\\log(')
    .replace(/\bsqrt\(/gi, '\\sqrt{')
    .replace(/√\(/g, '\\sqrt{')
    .replace(/\bpi\b/gi, '\\pi')
    .replace(/π/g, '\\pi')
    .replace(/\*/g, '\\cdot ')
    .replace(/\^(\d)/g, '^{$1}');
}

function evaluateSimple(expr: string, x: number): string {
  try {
    const jsExpr = expr
      .replace(/\^/g, '**')
      .replace(/sin\(/gi, 'Math.sin(')
      .replace(/cos\(/gi, 'Math.cos(')
      .replace(/tan\(/gi, 'Math.tan(')
      .replace(/ln\(/gi, 'Math.log(')
      .replace(/log\(/gi, 'Math.log10(')
      .replace(/√\(/g, 'Math.sqrt(')
      .replace(/sqrt\(/gi, 'Math.sqrt(')
      .replace(/π/g, 'Math.PI')
      .replace(/pi/gi, 'Math.PI')
      .replace(/\|([^|]+)\|/g, 'Math.abs($1)')
      .replace(/e\^/g, 'Math.exp(')
      .replace(/\bx\b/g, `(${x})`);
    const result = Function(`"use strict"; return (${jsExpr})`)();
    if (typeof result !== 'number' || !isFinite(result)) return '—';
    return Number(result.toFixed(4)).toString();
  } catch {
    return '—';
  }
}

// ── Styles ───────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: TI.bg },

  // Mode bar
  modeBar: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    paddingVertical: 6,
    gap: 6,
    borderBottomWidth: 1,
    borderBottomColor: TI.border,
  },
  modeBtn: {
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 8,
    backgroundColor: TI.bgLight,
  },
  modeBtnActive: {
    backgroundColor: TI.accent,
  },
  modeBtnHighlight: {
    borderWidth: 1,
    borderColor: TI.accent + '60',
  },
  modeBtnText: {
    fontSize: 13,
    fontWeight: '700',
    color: TI.textDim,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  modeBtnTextActive: {
    color: '#FFF',
  },
  mode2ndBtn: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    backgroundColor: TI.bgKey2nd + '30',
  },
  mode2ndText: {
    fontSize: 12,
    fontWeight: '700',
    color: TI.bgKey2nd,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  mode2ndActive: {
    color: '#FFF',
  },

  // Screen area (graph / Y= / table)
  screenArea: {
    flex: 1,
    backgroundColor: TI.display,
  },
  emptyGraph: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
  },
  emptyGraphText: {
    fontSize: 13,
    color: '#555',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },

  // Y= Editor
  yEditContainer: {
    flex: 1,
    padding: 12,
    gap: 6,
  },
  yEditTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: TI.textDim,
    marginBottom: 4,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  yEditRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 10,
    paddingVertical: 10,
    borderRadius: 10,
    backgroundColor: TI.bgLight,
    borderWidth: 1,
    borderColor: 'transparent',
  },
  yEditRowActive: {
    borderColor: TI.accent,
    backgroundColor: TI.accent + '15',
  },
  yEditToggle: {
    padding: 2,
  },
  yEditDot: {
    width: 20,
    height: 20,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  yEditLabel: {
    fontSize: 15,
    fontWeight: '700',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    width: 36,
  },
  yEditExprWrap: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  yEditExpr: {
    fontSize: 16,
    color: TI.text,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  yEditExprPlaceholder: {
    color: '#444',
    fontStyle: 'italic',
  },
  yEditCursor: {
    width: 2,
    height: 20,
    backgroundColor: TI.accent,
    marginLeft: 1,
  },
  yEditHint: {
    fontSize: 11,
    color: '#555',
    marginTop: 12,
    lineHeight: 16,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },

  // Table
  tableContainer: {
    flex: 1,
    padding: 8,
  },
  tableHeader: {
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderBottomColor: TI.border,
    paddingBottom: 6,
    marginBottom: 4,
  },
  tableRow: {
    flexDirection: 'row',
    paddingVertical: 4,
    borderBottomWidth: 1,
    borderBottomColor: TI.border + '40',
  },
  tableCell: {
    flex: 1,
    fontSize: 13,
    color: TI.text,
    textAlign: 'center',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  tableCellHeader: {
    fontWeight: '700',
    color: TI.textDim,
  },

  // Keypad
  keypad: {
    backgroundColor: TI.bg,
    paddingHorizontal: 6,
    paddingTop: 6,
    gap: 4,
    borderTopWidth: 1,
    borderTopColor: TI.border,
  },
  keyRow: {
    flexDirection: 'row',
    gap: 4,
    justifyContent: 'center',
  },
  key: {
    flex: 1,
    height: 42,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    maxWidth: (SCREEN_WIDTH - 32) / 5,
    borderWidth: 1,
    borderColor: '#E5E7EB',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  keyWide: {
    flex: 2,
    maxWidth: ((SCREEN_WIDTH - 32) / 5) * 2 + 4,
  },
  keyText: {
    fontSize: 15,
    fontWeight: '600',
    color: TI.text,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  keyTextSmall: {
    fontSize: 11,
  },
});
