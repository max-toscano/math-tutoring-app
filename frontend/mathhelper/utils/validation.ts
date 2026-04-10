export interface PasswordValidation {
  minLength: boolean;
  hasUppercase: boolean;
  hasLowercase: boolean;
  hasNumber: boolean;
  hasSpecial: boolean;
  strength: number;
}

export interface DisplayNameValidation {
  minLength: boolean;
  maxLength: boolean;
  noSpaces: boolean;
  validChars: boolean;
}

export function validatePassword(pw: string): PasswordValidation {
  const minLength = pw.length >= 8;
  const hasUppercase = /[A-Z]/.test(pw);
  const hasLowercase = /[a-z]/.test(pw);
  const hasNumber = /[0-9]/.test(pw);
  const hasSpecial = /[^A-Za-z0-9]/.test(pw);

  const strength = [minLength, hasUppercase, hasLowercase, hasNumber, hasSpecial].filter(Boolean).length;

  // Map 5 booleans to a 0-4 score: 0-1 = 0, 2 = 1, 3 = 2, 4 = 3, 5 = 4
  const score = Math.max(0, strength - 1);

  return {
    minLength,
    hasUppercase,
    hasLowercase,
    hasNumber,
    hasSpecial,
    strength: score,
  };
}

export function validateDisplayName(name: string): DisplayNameValidation {
  return {
    minLength: name.length >= 3,
    maxLength: name.length <= 20,
    noSpaces: !/\s/.test(name),
    validChars: /^[a-zA-Z0-9_]*$/.test(name) && name.length > 0,
  };
}

export function getPasswordStrengthLabel(score: number): 'Weak' | 'Fair' | 'Good' | 'Strong' {
  if (score <= 1) return 'Weak';
  if (score === 2) return 'Fair';
  if (score === 3) return 'Good';
  return 'Strong';
}
