/**
 * calculator.tsx
 * Scientific calculator with TI-84 features — white & purple theme.
 * Full-screen layout: display flexes to fill top, keypad fills bottom edge-to-edge.
 */

import { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Platform,
  Dimensions,
  ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Colors } from '../../constants/Colors';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');
const MONO = Platform.OS === 'ios' ? 'Menlo' : 'monospace';

// Total keypad rows: 4 sci + 1 divider + 5 num = ~10 visual rows
// Calculate button heights to fill available space evenly
const GAP = 5;

interface HistoryEntry { expression: string; result: string; }

// ═══════════════════════════════════════════════════════════════════════
// COMPONENTS
// ═══════════════════════════════════════════════════════════════════════

function CalcBtn({
  label, onPress, bg, color, size = 14, bold, icon, flex = 1,
}: {
  label: string; onPress: () => void; bg: string; color: string;
  size?: number; bold?: boolean; icon?: string; flex?: number;
}) {
  return (
    <TouchableOpacity
      style={[st.btn, { backgroundColor: bg, flex }]}
      onPress={onPress}
      activeOpacity={0.5}
    >
      {icon ? (
        <Ionicons name={icon as any} size={size + 2} color={color} />
      ) : (
        <Text style={[st.btnText, { color, fontSize: size }, bold && { fontWeight: '700' }]}>
          {label}
        </Text>
      )}
    </TouchableOpacity>
  );
}

function Row({ children }: { children: React.ReactNode }) {
  return <View style={st.row}>{children}</View>;
}

function SciBtn({
  label, secondLabel, onPress, active,
}: {
  label: string; secondLabel?: string; onPress: () => void; active?: boolean;
}) {
  return (
    <View style={st.sciBtnWrap}>
      {secondLabel ? (
        <Text style={st.secLabel} numberOfLines={1}>{secondLabel}</Text>
      ) : (
        <View style={st.secSpacer} />
      )}
      <TouchableOpacity
        style={[st.btn, st.sciBtn, active && { backgroundColor: Colors.primary }]}
        onPress={onPress}
        activeOpacity={0.5}
      >
        <Text style={[st.btnText, { fontSize: 12, color: active ? '#FFF' : Colors.text }]}>
          {label}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

// ═══════════════════════════════════════════════════════════════════════
// MAIN SCREEN
// ═══════════════════════════════════════════════════════════════════════

export default function CalculatorScreen() {
  const insets = useSafeAreaInsets();

  const [expression, setExpression] = useState('');
  const [display, setDisplay] = useState('0');
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [isRadians, setIsRadians] = useState(true);
  const [is2nd, setIs2nd] = useState(false);
  const [memory, setMemory] = useState(0);
  const [hasMemory, setHasMemory] = useState(false);
  const [justEvaluated, setJustEvaluated] = useState(false);

  function append(text: string) {
    if (justEvaluated) {
      const isOp = ['+', '-', '×', '÷', '*', '/', '^', 'mod'].includes(text);
      if (!isOp) { setExpression(text); setDisplay(''); setJustEvaluated(false); return; }
      setJustEvaluated(false);
    }
    setExpression((prev) => prev + text);
  }
  function appendFunc(name: string) {
    if (justEvaluated) { setExpression(name + '(' + expression + ')'); setJustEvaluated(false); return; }
    append(name + '(');
  }
  function handleBackspace() {
    if (justEvaluated) { handleClear(); return; }
    setExpression((prev) => {
      const pats = ['arcsin(','arccos(','arctan(','sinh(','cosh(','tanh(',
        'sin(','cos(','tan(','ln(','log(','log₂(','abs(','√(','³√('];
      for (const p of pats) { if (prev.endsWith(p)) return prev.slice(0, -p.length); }
      return prev.slice(0, -1);
    });
  }
  function handleClear() { setExpression(''); setDisplay('0'); setJustEvaluated(false); }
  function handleEquals() {
    if (!expression.trim()) return;
    try {
      const result = evaluate(expression, isRadians);
      const formatted = formatResult(result);
      setHistory((prev) => [{ expression, result: formatted }, ...prev].slice(0, 50));
      setDisplay(formatted); setExpression(formatted); setJustEvaluated(true);
    } catch { setDisplay('Error'); setJustEvaluated(true); }
  }
  function handleNegate() {
    if (!expression) return;
    if (expression.startsWith('(-')) setExpression(expression.slice(2).replace(/^\)/, ''));
    else setExpression('(-' + expression + ')');
  }
  function memClear() { setMemory(0); setHasMemory(false); }
  function memRecall() { if (hasMemory) append(memory.toString()); }
  function memAdd() { try { setMemory((m) => m + evaluate(expression || display, isRadians)); setHasMemory(true); } catch {} }
  function memSub() { try { setMemory((m) => m - evaluate(expression || display, isRadians)); setHasMemory(true); } catch {} }

  const prettyExpr = expression
    .replace(/\*/g, '×').replace(/\//g, '÷').replace(/pi/g, 'π').replace(/euler/g, 'e');

  return (
    <View style={[st.container, { paddingTop: insets.top, paddingBottom: insets.bottom }]}>

      {/* ══════════ DISPLAY ══════════ */}
      <View style={st.display}>
        {/* Status */}
        <View style={st.statusRow}>
          <View style={[st.chip, is2nd && st.chipOn]}>
            <Text style={[st.chipText, is2nd && st.chipTextOn]}>2ND</Text>
          </View>
          <View style={[st.chip, st.chipOn]}>
            <Text style={st.chipTextOn}>{isRadians ? 'RAD' : 'DEG'}</Text>
          </View>
          {hasMemory && <View style={[st.chip, st.chipOn]}><Text style={st.chipTextOn}>M</Text></View>}
        </View>

        {/* History */}
        <ScrollView style={st.histScroll} showsVerticalScrollIndicator={false}>
          {history.slice(0, 3).reverse().map((h, i) => (
            <TouchableOpacity key={i} onPress={() => { setExpression(h.result); setDisplay(h.result); setJustEvaluated(true); }} activeOpacity={0.6}>
              <Text style={st.histExpr} numberOfLines={1}>{h.expression}</Text>
              <Text style={st.histAns} numberOfLines={1}>{h.result}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        {/* Expression */}
        <View style={st.exprRow}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ alignItems: 'center' }}>
            <Text style={st.exprText}>{prettyExpr || ' '}</Text>
            <View style={st.cursor} />
          </ScrollView>
        </View>

        {/* Result */}
        <Text style={[st.resultText, display.length > 10 && { fontSize: 34 }, display.length > 14 && { fontSize: 26 }]}
          numberOfLines={1} adjustsFontSizeToFit>
          {display}
        </Text>
      </View>

      {/* ══════════ KEYPAD ══════════ */}
      <View style={st.keypad}>

        {/* Utility: 2nd, RAD/DEG, Memory */}
        <Row>
          <CalcBtn label="2nd" onPress={() => setIs2nd((p) => !p)}
            bg={is2nd ? Colors.primary : '#EDE9FF'} color={is2nd ? '#FFF' : Colors.primary} size={11} bold />
          <CalcBtn label={isRadians ? 'RAD' : 'DEG'} onPress={() => setIsRadians((p) => !p)}
            bg="#EDE9FF" color={Colors.primary} size={10} bold />
          <CalcBtn label="MC" onPress={memClear} bg="#F0F0F6" color={Colors.textLight} size={10} />
          <CalcBtn label="MR" onPress={memRecall} bg="#F0F0F6" color={hasMemory ? Colors.primary : Colors.textLight} size={10} />
          <CalcBtn label="M+" onPress={memAdd} bg="#F0F0F6" color={Colors.textLight} size={10} />
          <CalcBtn label="M−" onPress={memSub} bg="#F0F0F6" color={Colors.textLight} size={10} />
        </Row>

        {/* Sci Row 1: Trig + Logs */}
        <Row>
          <SciBtn label={is2nd ? 'sin⁻¹' : 'sin'} secondLabel={is2nd ? '' : 'sin⁻¹'}
            onPress={() => appendFunc(is2nd ? 'arcsin' : 'sin')} />
          <SciBtn label={is2nd ? 'cos⁻¹' : 'cos'} secondLabel={is2nd ? '' : 'cos⁻¹'}
            onPress={() => appendFunc(is2nd ? 'arccos' : 'cos')} />
          <SciBtn label={is2nd ? 'tan⁻¹' : 'tan'} secondLabel={is2nd ? '' : 'tan⁻¹'}
            onPress={() => appendFunc(is2nd ? 'arctan' : 'tan')} />
          <SciBtn label={is2nd ? 'eˣ' : 'ln'} secondLabel={is2nd ? '' : 'eˣ'}
            onPress={() => is2nd ? append('euler^') : appendFunc('ln')} />
          <SciBtn label={is2nd ? 'log₂' : 'log'} secondLabel={is2nd ? '' : 'log₂'}
            onPress={() => appendFunc(is2nd ? 'log₂' : 'log')} />
        </Row>

        {/* Sci Row 2: Powers, roots, special */}
        <Row>
          <SciBtn label={is2nd ? '³√' : '√'} secondLabel={is2nd ? '' : '³√'}
            onPress={() => appendFunc(is2nd ? '³√' : '√')} />
          <SciBtn label={is2nd ? 'x³' : 'x²'} secondLabel={is2nd ? '' : 'x³'}
            onPress={() => append(is2nd ? '^3' : '^2')} />
          <SciBtn label="xⁿ" onPress={() => append('^')} />
          <SciBtn label="x!" secondLabel="|x|"
            onPress={() => is2nd ? appendFunc('abs') : append('!')} />
          <SciBtn label={is2nd ? 'mod' : '%'} secondLabel={is2nd ? '' : 'mod'}
            onPress={() => is2nd ? append('mod') : append('%')} />
        </Row>

        {/* Constants, parens, ANS */}
        <Row>
          <CalcBtn label="π" onPress={() => append('pi')} bg="#EDE9FF" color={Colors.primary} size={15} bold />
          <CalcBtn label="e" onPress={() => append('euler')} bg="#EDE9FF" color={Colors.primary} size={14} bold />
          <CalcBtn label="(" onPress={() => append('(')} bg="#F0F0F6" color={Colors.text} size={16} />
          <CalcBtn label=")" onPress={() => append(')')} bg="#F0F0F6" color={Colors.text} size={16} />
          <CalcBtn label="ANS" onPress={() => { if (history.length > 0) append(history[0].result); }}
            bg="#EDE9FF" color={Colors.primary} size={10} bold />
        </Row>

        {/* Divider */}
        <View style={st.divider} />

        {/* DEL CLR (−) ÷ */}
        <Row>
          <CalcBtn label="" onPress={handleBackspace} icon="backspace-outline" bg="#FFF0F0" color="#FF6B6B" size={16} />
          <CalcBtn label="CLR" onPress={handleClear} bg="#FFF0F0" color="#FF6B6B" size={13} bold />
          <CalcBtn label="(−)" onPress={handleNegate} bg="#F0F0F6" color={Colors.text} size={13} />
          <CalcBtn label="÷" onPress={() => append('/')} bg={Colors.primary} color="#FFF" size={20} bold />
        </Row>

        {/* 7 8 9 × */}
        <Row>
          <CalcBtn label="7" onPress={() => append('7')} bg="#FFF" color={Colors.text} size={20} />
          <CalcBtn label="8" onPress={() => append('8')} bg="#FFF" color={Colors.text} size={20} />
          <CalcBtn label="9" onPress={() => append('9')} bg="#FFF" color={Colors.text} size={20} />
          <CalcBtn label="×" onPress={() => append('*')} bg={Colors.primary} color="#FFF" size={18} bold />
        </Row>

        {/* 4 5 6 − */}
        <Row>
          <CalcBtn label="4" onPress={() => append('4')} bg="#FFF" color={Colors.text} size={20} />
          <CalcBtn label="5" onPress={() => append('5')} bg="#FFF" color={Colors.text} size={20} />
          <CalcBtn label="6" onPress={() => append('6')} bg="#FFF" color={Colors.text} size={20} />
          <CalcBtn label="−" onPress={() => append('-')} bg={Colors.primary} color="#FFF" size={20} bold />
        </Row>

        {/* 1 2 3 + */}
        <Row>
          <CalcBtn label="1" onPress={() => append('1')} bg="#FFF" color={Colors.text} size={20} />
          <CalcBtn label="2" onPress={() => append('2')} bg="#FFF" color={Colors.text} size={20} />
          <CalcBtn label="3" onPress={() => append('3')} bg="#FFF" color={Colors.text} size={20} />
          <CalcBtn label="+" onPress={() => append('+')} bg={Colors.primary} color="#FFF" size={20} bold />
        </Row>

        {/* 0 . = */}
        <Row>
          <CalcBtn label="0" onPress={() => append('0')} bg="#FFF" color={Colors.text} size={20} flex={2} />
          <CalcBtn label="." onPress={() => append('.')} bg="#FFF" color={Colors.text} size={20} />
          <CalcBtn label="=" onPress={handleEquals} bg={Colors.primaryDark} color="#FFF" size={20} bold />
        </Row>
      </View>
    </View>
  );
}

// ═══════════════════════════════════════════════════════════════════════
// EVALUATOR (preserved)
// ═══════════════════════════════════════════════════════════════════════

function evaluate(expr: string, radians: boolean): number {
  let e = expr.replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
  e = e.replace(/\bpi\b/g, `(${Math.PI})`);
  e = e.replace(/\beuler\b/g, `(${Math.E})`);
  e = e.replace(/(\d+\.?\d*)%/g, '($1/100)');
  e = e.replace(/mod/g, '%');
  e = e.replace(/(\d+)!/g, '_fact($1)');
  e = e.replace(/arcsin\(/g, '_asin(');
  e = e.replace(/arccos\(/g, '_acos(');
  e = e.replace(/arctan\(/g, '_atan(');
  e = e.replace(/sinh\(/g, 'Math.sinh(');
  e = e.replace(/cosh\(/g, 'Math.cosh(');
  e = e.replace(/tanh\(/g, 'Math.tanh(');
  e = e.replace(/sin\(/g, '_sin(');
  e = e.replace(/cos\(/g, '_cos(');
  e = e.replace(/tan\(/g, '_tan(');
  e = e.replace(/log₂\(/g, '_log2(');
  e = e.replace(/log\(/g, '_log10(');
  e = e.replace(/ln\(/g, 'Math.log(');
  e = e.replace(/³√\(/g, '_cbrt(');
  e = e.replace(/√\(/g, 'Math.sqrt(');
  e = e.replace(/abs\(/g, 'Math.abs(');
  e = e.replace(/(\d)\(/g, '$1*(');
  e = e.replace(/\)\(/g, ')*(');
  e = e.replace(/\^/g, '**');
  const fn = new Function(
    '_sin','_cos','_tan','_asin','_acos','_atan','_log10','_log2','_cbrt','_fact',
    `"use strict"; return (${e});`
  );
  const toRad = radians ? (x: number) => x : (x: number) => x * Math.PI / 180;
  const fromRad = radians ? (x: number) => x : (x: number) => x * 180 / Math.PI;
  const result = fn(
    (x: number) => Math.sin(toRad(x)), (x: number) => Math.cos(toRad(x)),
    (x: number) => Math.tan(toRad(x)), (x: number) => fromRad(Math.asin(x)),
    (x: number) => fromRad(Math.acos(x)), (x: number) => fromRad(Math.atan(x)),
    (x: number) => Math.log10(x), (x: number) => Math.log2(x),
    (x: number) => Math.cbrt(x), (x: number) => factorial(x),
  );
  if (typeof result !== 'number' || !isFinite(result)) throw new Error('Invalid');
  return result;
}

function factorial(n: number): number {
  if (n < 0 || n !== Math.floor(n)) throw new Error('Invalid');
  if (n > 170) return Infinity;
  let r = 1; for (let i = 2; i <= n; i++) r *= i; return r;
}

function formatResult(val: number): string {
  if (!isFinite(val)) return 'Error';
  if (val === 0) return '0';
  if (Number.isInteger(val) && Math.abs(val) < 1e15) return val.toString();
  const str = parseFloat(val.toPrecision(12)).toString();
  return str.length > 14 ? val.toExponential(8) : str;
}

// ═══════════════════════════════════════════════════════════════════════
// STYLES
// ═══════════════════════════════════════════════════════════════════════

const st = StyleSheet.create({
  // Full-screen container — no margins, no padding except safe area
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },

  // Display takes remaining space above keypad
  display: {
    flex: 1,
    paddingHorizontal: 16,
    paddingTop: 8,
    justifyContent: 'flex-end',
  },
  statusRow: {
    flexDirection: 'row',
    gap: 6,
    marginBottom: 6,
  },
  chip: {
    paddingHorizontal: 7,
    paddingVertical: 2,
    borderRadius: 4,
    backgroundColor: '#F5F5FA',
  },
  chipOn: {
    backgroundColor: '#EDE9FF',
  },
  chipText: {
    fontSize: 9, fontWeight: '700', color: Colors.textMuted, fontFamily: MONO, letterSpacing: 0.5,
  },
  chipTextOn: {
    fontSize: 9, fontWeight: '800', color: Colors.primary, fontFamily: MONO, letterSpacing: 0.5,
  },
  histScroll: {
    maxHeight: 48,
    marginBottom: 2,
  },
  histExpr: {
    fontSize: 11, color: Colors.textMuted, fontFamily: MONO, textAlign: 'right',
  },
  histAns: {
    fontSize: 12, color: Colors.textLight, fontFamily: MONO, textAlign: 'right', marginBottom: 2,
  },
  exprRow: {
    marginBottom: 2,
  },
  exprText: {
    fontSize: 18, color: Colors.text, fontFamily: MONO, fontWeight: '500',
  },
  cursor: {
    width: 2, height: 20, backgroundColor: Colors.primary, marginLeft: 1, borderRadius: 1,
  },
  resultText: {
    fontSize: 44, fontWeight: '300', color: Colors.text, fontFamily: MONO, textAlign: 'right',
    marginBottom: 8,
  },

  // Keypad fills bottom — no scroll, all rows visible, edge-to-edge
  keypad: {
    paddingHorizontal: 6,
    gap: GAP,
    paddingBottom: 4,
  },

  // Each row stretches full width, even gap between buttons
  row: {
    flexDirection: 'row',
    gap: GAP,
  },

  // Buttons fill available flex space equally
  btn: {
    height: 44,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  btnText: {
    fontFamily: MONO, fontWeight: '600', textAlign: 'center',
  },

  // Scientific button wrapper (includes 2nd label)
  sciBtnWrap: {
    flex: 1,
    alignItems: 'stretch',
  },
  sciBtn: {
    backgroundColor: '#F0F0F6',
    height: 36,
  },
  secLabel: {
    fontSize: 8, fontWeight: '700', color: Colors.primary, fontFamily: MONO,
    height: 11, textAlign: 'center',
  },
  secSpacer: {
    height: 11,
  },

  // Thin divider between sci and numpad
  divider: {
    height: 1, backgroundColor: '#EDE9FF', marginHorizontal: 2,
  },
});
