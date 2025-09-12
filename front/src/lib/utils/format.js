/**
 * @fileoverview Formatting utilities for display and user interface
 */

/**
 * Format currency amounts with proper localization
 */
export function formatCurrency(amount, currency = 'USD', locale = 'en-US') {
  if (amount === null || amount === undefined) return '';
  
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(amount);
}

/**
 * Format numbers with appropriate decimal places and separators
 */
export function formatNumber(number, options = {}) {
  if (number === null || number === undefined) return '';
  
  const {
    locale = 'en-US',
    minimumFractionDigits = 0,
    maximumFractionDigits = 2,
    notation = 'standard'
  } = options;

  return new Intl.NumberFormat(locale, {
    minimumFractionDigits,
    maximumFractionDigits,
    notation
  }).format(number);
}

/**
 * Format large numbers with abbreviations (K, M, B)
 */
export function formatCompactNumber(number, locale = 'en-US') {
  if (number === null || number === undefined) return '';
  
  return new Intl.NumberFormat(locale, {
    notation: 'compact',
    maximumFractionDigits: 1
  }).format(number);
}

/**
 * Format dates with flexible options and relative time
 */
export function formatDate(date, options = {}) {
  if (!date) return '';
  
  const {
    locale = 'en-US',
    dateStyle = 'medium',
    timeStyle,
    relative = false,
    ...customOptions
  } = options;

  const dateObj = new Date(date);
  
  if (isNaN(dateObj.getTime())) return '';

  // Relative time formatting
  if (relative) {
    return formatRelativeTime(dateObj, locale);
  }

  // Use dateStyle/timeStyle for modern formatting
  if (dateStyle || timeStyle) {
    const formatOptions = {};
    if (dateStyle) formatOptions.dateStyle = dateStyle;
    if (timeStyle) formatOptions.timeStyle = timeStyle;
    
    return new Intl.DateTimeFormat(locale, formatOptions).format(dateObj);
  }

  // Fallback to custom options
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    ...customOptions
  }).format(dateObj);
}

/**
 * Format relative time (e.g., "2 hours ago", "in 3 days")
 */
export function formatRelativeTime(date, locale = 'en-US') {
  if (!date) return '';
  
  const dateObj = new Date(date);
  const now = new Date();
  const diffInSeconds = Math.floor((now - dateObj) / 1000);

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'week', seconds: 604800 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
    { label: 'second', seconds: 1 }
  ];

  for (const interval of intervals) {
    const count = Math.floor(Math.abs(diffInSeconds) / interval.seconds);
    if (count >= 1) {
      return rtf.format(diffInSeconds < 0 ? count : -count, interval.label);
    }
  }

  return rtf.format(0, 'second');
}

/**
 * Format duration in human-readable format
 */
export function formatDuration(seconds) {
  if (!seconds || seconds < 0) return '0s';

  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  const parts = [];
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  if (secs > 0) parts.push(`${secs}s`);

  return parts.join(' ') || '0s';
}

/**
 * Truncate text with smart word boundaries
 */
export function truncateText(text, maxLength = 100, suffix = '...') {
  if (!text || text.length <= maxLength) return text || '';
  
  const truncated = text.substring(0, maxLength - suffix.length);
  const lastSpace = truncated.lastIndexOf(' ');
  
  // If we can find a space and it's not too close to the beginning, break at word boundary
  if (lastSpace > maxLength * 0.7) {
    return truncated.substring(0, lastSpace) + suffix;
  }
  
  return truncated + suffix;
}

/**
 * Calculate and format discount percentage
 */
export function formatDiscount(price, comparePrice) {
  if (!comparePrice || comparePrice <= price || price < 0) return 0;
  return Math.round(((comparePrice - price) / comparePrice) * 100);
}

/**
 * Format file sizes in human-readable format
 */
export function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 B';
  
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Format phone numbers with proper formatting
 */
export function formatPhoneNumber(phoneNumber, format = 'US') {
  if (!phoneNumber) return '';
  
  // Remove all non-digit characters
  const digits = phoneNumber.replace(/\D/g, '');
  
  if (format === 'US' && digits.length === 10) {
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
  } else if (format === 'US' && digits.length === 11 && digits[0] === '1') {
    return `+1 (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7)}`;
  }
  
  return phoneNumber; // Return original if format not recognized
}

/**
 * Format postal codes with proper spacing
 */
export function formatPostalCode(code, country = 'US') {
  if (!code) return '';
  
  const cleanCode = code.replace(/\s/g, '').toUpperCase();
  
  switch (country) {
    case 'CA': // Canadian postal code format: A1A 1A1
      if (cleanCode.length === 6) {
        return `${cleanCode.slice(0, 3)} ${cleanCode.slice(3)}`;
      }
      break;
    case 'UK': // UK postal code format varies, but typically has space
      if (cleanCode.length >= 5) {
        return `${cleanCode.slice(0, -3)} ${cleanCode.slice(-3)}`;
      }
      break;
    case 'US':
    default:
      return cleanCode; // US postal codes don't typically have spaces
  }
  
  return code;
}

/**
 * Format addresses for display
 */
export function formatAddress(address) {
  if (!address) return '';
  
  const parts = [
    address.street,
    address.city,
    address.state && address.zipCode ? `${address.state} ${address.zipCode}` : address.state || address.zipCode,
    address.country
  ].filter(Boolean);
  
  return parts.join(', ');
}

/**
 * Format percentages with proper decimal places
 */
export function formatPercentage(value, decimals = 1) {
  if (value === null || value === undefined) return '';
  return `${(value * 100).toFixed(decimals)}%`;
}

/**
 * Format rating with stars or numeric display
 */
export function formatRating(rating, maxRating = 5, format = 'numeric') {
  if (rating === null || rating === undefined) return '';
  
  if (format === 'stars') {
    const filled = '★'.repeat(Math.floor(rating));
    const empty = '☆'.repeat(maxRating - Math.floor(rating));
    return filled + empty;
  }
  
  return `${rating.toFixed(1)}/${maxRating}`;
}

/**
 * Format stock quantity with status indicators
 */
export function formatStock(quantity, threshold = { low: 10, out: 0 }) {
  if (quantity === null || quantity === undefined) return { text: 'Unknown', status: 'unknown' };
  
  if (quantity <= threshold.out) {
    return { text: 'Out of Stock', status: 'out' };
  } else if (quantity <= threshold.low) {
    return { text: `Only ${quantity} left`, status: 'low' };
  } else {
    return { text: 'In Stock', status: 'in' };
  }
}

/**
 * Format color values to display format
 */
export function formatColor(color) {
  if (!color) return '';
  
  // Convert hex to readable name if possible
  const colorNames = {
    '#000000': 'Black',
    '#ffffff': 'White',
    '#ff0000': 'Red',
    '#00ff00': 'Green',
    '#0000ff': 'Blue',
    // Add more as needed
  };
  
  return colorNames[color.toLowerCase()] || color.toUpperCase();
}

// Aliases for common formatting needs
export const formatPrice = formatCurrency;