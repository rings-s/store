/**
 * @fileoverview Comprehensive validation utilities for forms and user input
 */

import { VALIDATION_RULES } from './constants.js';

/**
 * Validation result structure
 * @typedef {Object} ValidationResult
 * @property {boolean} valid - Whether the input is valid
 * @property {string} message - Error message if invalid
 * @property {string} field - Field name for context
 */

/**
 * Create a validation result object
 */
function createValidationResult(valid, message = '', field = '') {
  return { valid, message, field };
}

/**
 * Email validation with comprehensive rules
 */
export function validateEmail(email, field = 'email') {
  if (!email || typeof email !== 'string') {
    return createValidationResult(false, 'Email is required', field);
  }

  const trimmedEmail = email.trim();
  
  if (trimmedEmail.length === 0) {
    return createValidationResult(false, 'Email is required', field);
  }

  if (trimmedEmail.length > 254) {
    return createValidationResult(false, 'Email is too long', field);
  }

  if (!VALIDATION_RULES.EMAIL.PATTERN.test(trimmedEmail)) {
    return createValidationResult(false, VALIDATION_RULES.EMAIL.MESSAGE, field);
  }

  // Check for consecutive dots
  if (trimmedEmail.includes('..')) {
    return createValidationResult(false, 'Email cannot contain consecutive dots', field);
  }

  // Check for valid domain
  const parts = trimmedEmail.split('@');
  if (parts.length !== 2) {
    return createValidationResult(false, 'Email must contain exactly one @ symbol', field);
  }

  const [localPart, domain] = parts;
  
  if (localPart.length === 0 || localPart.length > 64) {
    return createValidationResult(false, 'Email local part is invalid', field);
  }

  if (domain.length === 0 || domain.length > 253) {
    return createValidationResult(false, 'Email domain is invalid', field);
  }

  return createValidationResult(true);
}

/**
 * Password validation with strength requirements
 */
export function validatePassword(password, field = 'password') {
  if (!password || typeof password !== 'string') {
    return createValidationResult(false, 'Password is required', field);
  }

  if (password.length < VALIDATION_RULES.PASSWORD.MIN_LENGTH) {
    return createValidationResult(false, `Password must be at least ${VALIDATION_RULES.PASSWORD.MIN_LENGTH} characters`, field);
  }

  if (password.length > 128) {
    return createValidationResult(false, 'Password is too long', field);
  }

  // Check for character requirements
  const hasLower = /[a-z]/.test(password);
  const hasUpper = /[A-Z]/.test(password);
  const hasDigit = /\d/.test(password);
  const hasSpecial = /[@$!%*?&]/.test(password);

  if (!hasLower || !hasUpper || !hasDigit || !hasSpecial) {
    return createValidationResult(false, VALIDATION_RULES.PASSWORD.MESSAGE, field);
  }

  // Check for common weak patterns
  const commonPatterns = [
    /(.)\1{2,}/, // Three or more consecutive identical characters
    /123|abc|qwe/i, // Sequential patterns
    /password|123456|qwerty/i // Common weak passwords
  ];

  for (const pattern of commonPatterns) {
    if (pattern.test(password)) {
      return createValidationResult(false, 'Password contains common weak patterns', field);
    }
  }

  return createValidationResult(true);
}

/**
 * Confirm password validation
 */
export function validatePasswordConfirm(password, confirmPassword, field = 'confirmPassword') {
  if (!confirmPassword || typeof confirmPassword !== 'string') {
    return createValidationResult(false, 'Password confirmation is required', field);
  }

  if (password !== confirmPassword) {
    return createValidationResult(false, 'Passwords do not match', field);
  }

  return createValidationResult(true);
}

/**
 * Phone number validation with flexible formats
 */
export function validatePhone(phone, field = 'phone') {
  if (!phone || typeof phone !== 'string') {
    return createValidationResult(false, 'Phone number is required', field);
  }

  const trimmedPhone = phone.trim();
  
  if (trimmedPhone.length === 0) {
    return createValidationResult(false, 'Phone number is required', field);
  }

  if (!VALIDATION_RULES.PHONE.PATTERN.test(trimmedPhone)) {
    return createValidationResult(false, VALIDATION_RULES.PHONE.MESSAGE, field);
  }

  // Remove all non-digit characters for length validation
  const digitsOnly = trimmedPhone.replace(/\D/g, '');
  
  if (digitsOnly.length < VALIDATION_RULES.PHONE.MIN_LENGTH) {
    return createValidationResult(false, `Phone number must have at least ${VALIDATION_RULES.PHONE.MIN_LENGTH} digits`, field);
  }

  if (digitsOnly.length > 15) {
    return createValidationResult(false, 'Phone number is too long', field);
  }

  return createValidationResult(true);
}

/**
 * Postal code validation with country support
 */
export function validatePostalCode(code, country = 'US', field = 'postalCode') {
  if (!code || typeof code !== 'string') {
    return createValidationResult(false, 'Postal code is required', field);
  }

  const trimmedCode = code.trim().toUpperCase();
  
  if (trimmedCode.length === 0) {
    return createValidationResult(false, 'Postal code is required', field);
  }

  // Country-specific validation
  const patterns = {
    US: /^\d{5}(-\d{4})?$/,
    CA: /^[A-Z]\d[A-Z] ?\d[A-Z]\d$/,
    UK: /^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$/,
    DE: /^\d{5}$/,
    FR: /^\d{5}$/,
    AU: /^\d{4}$/
  };

  const pattern = patterns[country];
  if (pattern && !pattern.test(trimmedCode)) {
    return createValidationResult(false, `Invalid ${country} postal code format`, field);
  }

  // Generic validation if country not supported
  if (!pattern) {
    if (trimmedCode.length < VALIDATION_RULES.POSTAL_CODE.MIN_LENGTH || 
        trimmedCode.length > VALIDATION_RULES.POSTAL_CODE.MAX_LENGTH) {
      return createValidationResult(false, VALIDATION_RULES.POSTAL_CODE.MESSAGE, field);
    }
  }

  return createValidationResult(true);
}

/**
 * Required field validation
 */
export function validateRequired(value, field = 'field') {
  if (value === null || value === undefined) {
    return createValidationResult(false, `${field} is required`, field);
  }

  if (typeof value === 'string' && value.trim().length === 0) {
    return createValidationResult(false, `${field} is required`, field);
  }

  if (Array.isArray(value) && value.length === 0) {
    return createValidationResult(false, `${field} is required`, field);
  }

  return createValidationResult(true);
}

/**
 * Name validation (first name, last name, etc.)
 */
export function validateName(name, field = 'name') {
  if (!name || typeof name !== 'string') {
    return createValidationResult(false, `${field} is required`, field);
  }

  const trimmedName = name.trim();
  
  if (trimmedName.length === 0) {
    return createValidationResult(false, `${field} is required`, field);
  }

  if (trimmedName.length < 2) {
    return createValidationResult(false, `${field} must be at least 2 characters`, field);
  }

  if (trimmedName.length > 50) {
    return createValidationResult(false, `${field} is too long`, field);
  }

  // Only allow letters, spaces, hyphens, and apostrophes
  const namePattern = /^[a-zA-Z\s\-']+$/;
  if (!namePattern.test(trimmedName)) {
    return createValidationResult(false, `${field} can only contain letters, spaces, hyphens, and apostrophes`, field);
  }

  return createValidationResult(true);
}

/**
 * URL validation
 */
export function validateUrl(url, field = 'url') {
  if (!url || typeof url !== 'string') {
    return createValidationResult(false, 'URL is required', field);
  }

  const trimmedUrl = url.trim();
  
  if (trimmedUrl.length === 0) {
    return createValidationResult(false, 'URL is required', field);
  }

  try {
    const urlObj = new URL(trimmedUrl);
    if (!['http:', 'https:'].includes(urlObj.protocol)) {
      return createValidationResult(false, 'URL must use HTTP or HTTPS protocol', field);
    }
  } catch {
    return createValidationResult(false, 'Please enter a valid URL', field);
  }

  return createValidationResult(true);
}

/**
 * Numeric validation with range support
 */
export function validateNumber(value, options = {}, field = 'number') {
  const { min, max, integer = false } = options;

  if (value === null || value === undefined || value === '') {
    return createValidationResult(false, 'Number is required', field);
  }

  const num = Number(value);
  
  if (isNaN(num)) {
    return createValidationResult(false, 'Must be a valid number', field);
  }

  if (integer && !Number.isInteger(num)) {
    return createValidationResult(false, 'Must be a whole number', field);
  }

  if (min !== undefined && num < min) {
    return createValidationResult(false, `Must be at least ${min}`, field);
  }

  if (max !== undefined && num > max) {
    return createValidationResult(false, `Must be no more than ${max}`, field);
  }

  return createValidationResult(true);
}

/**
 * Date validation
 */
export function validateDate(date, options = {}, field = 'date') {
  const { future = false, past = false, minAge, maxAge } = options;

  if (!date) {
    return createValidationResult(false, 'Date is required', field);
  }

  const dateObj = new Date(date);
  
  if (isNaN(dateObj.getTime())) {
    return createValidationResult(false, 'Please enter a valid date', field);
  }

  const now = new Date();
  
  if (future && dateObj <= now) {
    return createValidationResult(false, 'Date must be in the future', field);
  }

  if (past && dateObj >= now) {
    return createValidationResult(false, 'Date must be in the past', field);
  }

  if (minAge) {
    const minDate = new Date();
    minDate.setFullYear(minDate.getFullYear() - minAge);
    if (dateObj > minDate) {
      return createValidationResult(false, `Must be at least ${minAge} years old`, field);
    }
  }

  if (maxAge) {
    const maxDate = new Date();
    maxDate.setFullYear(maxDate.getFullYear() - maxAge);
    if (dateObj < maxDate) {
      return createValidationResult(false, `Cannot be more than ${maxAge} years old`, field);
    }
  }

  return createValidationResult(true);
}

/**
 * Credit card validation using Luhn algorithm
 */
export function validateCreditCard(cardNumber, field = 'cardNumber') {
  if (!cardNumber || typeof cardNumber !== 'string') {
    return createValidationResult(false, 'Card number is required', field);
  }

  // Remove all non-digit characters
  const digits = cardNumber.replace(/\D/g, '');
  
  if (digits.length < 13 || digits.length > 19) {
    return createValidationResult(false, 'Card number must be between 13 and 19 digits', field);
  }

  // Luhn algorithm
  let sum = 0;
  let isEven = false;

  for (let i = digits.length - 1; i >= 0; i--) {
    let digit = parseInt(digits[i]);

    if (isEven) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }

    sum += digit;
    isEven = !isEven;
  }

  if (sum % 10 !== 0) {
    return createValidationResult(false, 'Invalid card number', field);
  }

  return createValidationResult(true);
}

/**
 * Validate multiple fields using a schema
 */
export function validateSchema(data, schema) {
  const results = {};
  let isValid = true;

  for (const [field, rules] of Object.entries(schema)) {
    const value = data[field];
    
    for (const rule of rules) {
      const result = rule(value, field);
      if (!result.valid) {
        results[field] = result;
        isValid = false;
        break; // Stop at first validation error for this field
      }
    }
  }

  return {
    valid: isValid,
    errors: results
  };
}

/**
 * Create validation rule factories for common cases
 */
export const ValidationRules = {
  required: (field) => (value) => validateRequired(value, field),
  email: (field) => (value) => validateEmail(value, field),
  password: (field) => (value) => validatePassword(value, field),
  phone: (field) => (value) => validatePhone(value, field),
  name: (field) => (value) => validateName(value, field),
  number: (options, field) => (value) => validateNumber(value, options, field),
  minLength: (min, field) => (value) => {
    if (!value || value.length < min) {
      return createValidationResult(false, `${field} must be at least ${min} characters`, field);
    }
    return createValidationResult(true);
  },
  maxLength: (max, field) => (value) => {
    if (value && value.length > max) {
      return createValidationResult(false, `${field} must be no more than ${max} characters`, field);
    }
    return createValidationResult(true);
  }
};