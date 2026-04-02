/**
 * stepParser.ts - Parses AI responses into structured step objects
 */

export interface EnhancedStep {
  number: number;
  title: string;
  content: string;
  insight?: string;    // "Key insight: ..." or "[bulb] ..."
  warning?: string;    // "Watch out: ..." or "Common mistake: ..."
}

const STEP_PATTERNS = [
  /(?:^|\n)\s*(?:\*\*)?Step\s+(\d+)(?:\s*[:.])?(?:\*\*)?[\s:]*(.*?)(?=(?:\n\s*(?:\*\*)?Step\s+\d|\n\s*#{1,3}\s*Step\s+\d|$))/gis,
  /(?:^|\n)\s*#{1,3}\s*Step\s+(\d+)(?:\s*[:.])?[\s:]*(.*?)(?=(?:\n\s*#{1,3}\s*Step\s+\d|$))/gis,
];

const INSIGHT_PATTERN = /(?:key\s+insight|tip|remember|note):\s*(.+?)(?=\n\n|\n(?=[A-Z])|$)/gi;
const WARNING_PATTERN = /(?:watch\s+out|common\s+mistake|caution|warning):\s*(.+?)(?=\n\n|\n(?=[A-Z])|$)/gi;

export function parseEnhancedSteps(text: string): EnhancedStep[] | null {
  for (const pattern of STEP_PATTERNS) {
    pattern.lastIndex = 0;
    const steps: EnhancedStep[] = [];
    let match;

    while ((match = pattern.exec(text)) !== null) {
      const number = parseInt(match[1], 10);
      const rest = match[2]?.trim() || '';

      const lines = rest.split('\n');
      const title = lines[0]
        ?.replace(/^\*\*|\*\*$/g, '')
        .replace(/^[:.\s]+/, '')
        .trim() || `Step ${number}`;
      const content = lines.slice(1).join('\n').trim() || rest;

      // Extract insight and warning
      let insight: string | undefined;
      let warning: string | undefined;

      INSIGHT_PATTERN.lastIndex = 0;
      const insightMatch = INSIGHT_PATTERN.exec(content);
      if (insightMatch) {
        insight = insightMatch[1].trim();
      }

      WARNING_PATTERN.lastIndex = 0;
      const warningMatch = WARNING_PATTERN.exec(content);
      if (warningMatch) {
        warning = warningMatch[1].trim();
      }

      steps.push({ number, title, content, insight, warning });
    }

    if (steps.length >= 2) {
      return steps;
    }
  }

  // Fallback: numbered list
  const numberedPattern = /(?:^|\n)\s*(\d+)\.\s+(.*?)(?=(?:\n\s*\d+\.\s|$))/gs;
  numberedPattern.lastIndex = 0;
  const steps: EnhancedStep[] = [];
  let match;

  while ((match = numberedPattern.exec(text)) !== null) {
    const number = parseInt(match[1], 10);
    const rest = match[2]?.trim() || '';
    const lines = rest.split('\n');
    const title = lines[0]?.replace(/^\*\*|\*\*$/g, '').trim() || `Step ${number}`;

    steps.push({ number, title, content: rest, insight: undefined, warning: undefined });
  }

  return steps.length >= 2 ? steps : null;
}
