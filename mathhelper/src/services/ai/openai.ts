/**
 * OpenAI service — uses the REST API directly via fetch so Metro bundler
 * does not need to resolve the openai npm package's ESM .mjs files.
 */
import { Platform } from 'react-native';

const OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions';

function getApiKey(): string {
  const key = process.env.EXPO_PUBLIC_OPENAI_API_KEY;
  if (!key) {
    throw new Error('EXPO_PUBLIC_OPENAI_API_KEY is not set. Add it to your .env file.');
  }
  return key;
}

export interface MathStep {
  step: number;
  title: string;
  explanation: string;
  math?: string;
}

export interface MathAnalysis {
  problem: string;
  topic: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  answer: string;
  steps: MathStep[];
  concepts: string[];
  tip: string;
}

const SYSTEM_PROMPT = `You are MathHelper AI, an expert mathematics tutor with mastery across all math subjects: arithmetic, algebra, geometry, trigonometry, calculus, linear algebra, number theory, probability, and statistics.

When given an image containing a math problem, you will:
1. Identify and state the problem clearly
2. Solve it correctly and completely
3. Break down the solution into clear, numbered steps
4. Identify the key mathematical concepts involved
5. Share a practical tip or common mistake to avoid

Respond ONLY with a valid JSON object — no markdown fences, no extra text. Use this exact schema:
{
  "problem": "The exact math problem as written or interpreted from the image",
  "topic": "Primary math topic (Algebra | Geometry | Calculus | Trigonometry | Statistics | Arithmetic | Number Theory | Linear Algebra)",
  "difficulty": "Easy | Medium | Hard",
  "answer": "The final answer stated concisely, e.g. 'x = 4' or 'Area = 49pi cm^2'",
  "steps": [
    {
      "step": 1,
      "title": "Short, descriptive step title",
      "explanation": "Thorough explanation of what is done in this step and why",
      "math": "The mathematical expression for this step in plain text (e.g. '2x + 5 - 5 = 13 - 5')"
    }
  ],
  "concepts": ["Key Concept 1", "Key Concept 2"],
  "tip": "A practical tip or common mistake students make with this type of problem"
}

Rules:
- Be thorough and educational — explain the reasoning behind every step
- Use plain text math notation (not LaTeX), e.g. write 'x^2' not '\\x^{2}', 'sqrt(x)' not '\\sqrt{x}'
- If no math problem is visible, set problem to "No math problem detected" and answer to "Please take a clearer photo"
- Output valid JSON only`;

async function imageUriToBase64(uri: string): Promise<{ base64: string; mimeType: string }> {
  if (Platform.OS === 'web') {
    const res = await fetch(uri);
    const blob = await res.blob();
    const mimeType = blob.type || 'image/jpeg';
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const dataUrl = reader.result as string;
        resolve({ base64: dataUrl.split(',')[1], mimeType });
      };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  } else {
    const FileSystem = await import('expo-file-system');
    const base64 = await FileSystem.readAsStringAsync(uri, {
      encoding: FileSystem.EncodingType.Base64,
    });
    const ext = uri.split('.').pop()?.toLowerCase() ?? 'jpg';
    return { base64, mimeType: ext === 'png' ? 'image/png' : 'image/jpeg' };
  }
}

export async function analyzeMathImage(imageUri: string): Promise<MathAnalysis> {
  const { base64, mimeType } = await imageUriToBase64(imageUri);

  const body = {
    model: 'gpt-4o',
    temperature: 0.2,
    max_tokens: 2500,
    response_format: { type: 'json_object' },
    messages: [
      { role: 'system', content: SYSTEM_PROMPT },
      {
        role: 'user',
        content: [
          {
            type: 'image_url',
            image_url: {
              url: `data:${mimeType};base64,${base64}`,
              detail: 'high',
            },
          },
          {
            type: 'text',
            text: 'Analyze the math problem in this image and provide a complete step-by-step solution.',
          },
        ],
      },
    ],
  };

  const response = await fetch(OPENAI_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${getApiKey()}`,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(
      (err as any)?.error?.message ?? `OpenAI request failed (${response.status})`
    );
  }

  const data = await response.json();
  const content: string = data?.choices?.[0]?.message?.content ?? '';

  if (!content) throw new Error('No response received from AI. Please try again.');

  try {
    return JSON.parse(content) as MathAnalysis;
  } catch {
    throw new Error('AI returned an unexpected format. Please try again.');
  }
}
