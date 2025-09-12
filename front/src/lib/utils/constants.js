/**
 * @fileoverview Application constants and configuration
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000/api',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3
};

// Application Information
export const APP_INFO = {
  NAME: 'Store',
  VERSION: '1.0.0',
  DESCRIPTION: 'Modern E-commerce Platform'
};

// Order Management
export const ORDER_STATUS = {
  PENDING: { 
    value: 'pending', 
    label: 'Pending', 
    color: 'warning',
    icon: 'clock',
    description: 'Order is waiting to be processed'
  },
  PROCESSING: { 
    value: 'processing', 
    label: 'Processing', 
    color: 'info',
    icon: 'cog',
    description: 'Order is being prepared'
  },
  SHIPPED: { 
    value: 'shipped', 
    label: 'Shipped', 
    color: 'primary',
    icon: 'truck',
    description: 'Order is on its way'
  },
  DELIVERED: { 
    value: 'delivered', 
    label: 'Delivered', 
    color: 'success',
    icon: 'check-circle',
    description: 'Order has been delivered'
  },
  CANCELLED: { 
    value: 'cancelled', 
    label: 'Cancelled', 
    color: 'error',
    icon: 'x-circle',
    description: 'Order has been cancelled'
  }
};

export const PAYMENT_STATUS = {
  PENDING: { value: 'pending', label: 'Pending', color: 'warning' },
  COMPLETED: { value: 'completed', label: 'Completed', color: 'success' },
  FAILED: { value: 'failed', label: 'Failed', color: 'error' },
  REFUNDED: { value: 'refunded', label: 'Refunded', color: 'info' }
};

// Product & Inventory
export const PRODUCT_STATUS = {
  DRAFT: { value: 'draft', label: 'Draft', color: 'gray' },
  ACTIVE: { value: 'active', label: 'Active', color: 'success' },
  ARCHIVED: { value: 'archived', label: 'Archived', color: 'warning' }
};

export const STOCK_STATUS = {
  IN_STOCK: { value: 'in_stock', label: 'In Stock', color: 'success' },
  LOW_STOCK: { value: 'low_stock', label: 'Low Stock', color: 'warning' },
  OUT_OF_STOCK: { value: 'out_of_stock', label: 'Out of Stock', color: 'error' }
};

// Sorting & Filtering
export const SORT_OPTIONS = [
  { value: 'name', label: 'Name: A-Z', icon: 'sort-alpha-down' },
  { value: '-name', label: 'Name: Z-A', icon: 'sort-alpha-up' },
  { value: 'price', label: 'Price: Low to High', icon: 'sort-numeric-down' },
  { value: '-price', label: 'Price: High to Low', icon: 'sort-numeric-up' },
  { value: '-created_at', label: 'Newest First', icon: 'sort-down' },
  { value: 'created_at', label: 'Oldest First', icon: 'sort-up' },
  { value: 'rating', label: 'Rating: Low to High', icon: 'star' },
  { value: '-rating', label: 'Rating: High to Low', icon: 'star' },
  { value: 'popularity', label: 'Most Popular', icon: 'trending-up' }
];

export const FILTER_OPTIONS = {
  PRICE_RANGES: [
    { min: 0, max: 25, label: 'Under $25' },
    { min: 25, max: 50, label: '$25 - $50' },
    { min: 50, max: 100, label: '$50 - $100' },
    { min: 100, max: 200, label: '$100 - $200' },
    { min: 200, max: null, label: '$200 & Above' }
  ],
  RATINGS: [
    { value: 5, label: '5 Stars', count: 0 },
    { value: 4, label: '4 Stars & Above', count: 0 },
    { value: 3, label: '3 Stars & Above', count: 0 },
    { value: 2, label: '2 Stars & Above', count: 0 },
    { value: 1, label: '1 Star & Above', count: 0 }
  ]
};

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 12,
  PAGE_SIZE_OPTIONS: [12, 24, 48, 96],
  MAX_VISIBLE_PAGES: 5
};

// UI Configuration
export const BREAKPOINTS = {
  SM: '640px',
  MD: '768px',
  LG: '1024px',
  XL: '1280px',
  '2XL': '1536px'
};

export const ANIMATIONS = {
  DURATION: {
    FAST: 150,
    DEFAULT: 300,
    SLOW: 500
  },
  EASING: {
    EASE_IN_OUT: 'cubic-bezier(0.4, 0, 0.2, 1)',
    EASE_OUT: 'cubic-bezier(0, 0, 0.2, 1)',
    EASE_IN: 'cubic-bezier(0.4, 0, 1, 1)',
    BOUNCE: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
  }
};

// Form Validation
export const VALIDATION_RULES = {
  EMAIL: {
    PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    MESSAGE: 'Please enter a valid email address'
  },
  PASSWORD: {
    MIN_LENGTH: 8,
    PATTERN: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
    MESSAGE: 'Password must be at least 8 characters with uppercase, lowercase, number and special character'
  },
  PHONE: {
    PATTERN: /^[\d\s\-\+\(\)]+$/,
    MIN_LENGTH: 10,
    MESSAGE: 'Please enter a valid phone number'
  },
  POSTAL_CODE: {
    MIN_LENGTH: 4,
    MAX_LENGTH: 10,
    MESSAGE: 'Please enter a valid postal code'
  }
};

// Local Storage Keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'accessToken',
  REFRESH_TOKEN: 'refreshToken',
  USER_PREFERENCES: 'userPreferences',
  CART: 'cart',
  WISHLIST: 'wishlist',
  RECENT_SEARCHES: 'recentSearches',
  THEME: 'theme'
};

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK: 'Network error. Please check your connection.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  SERVER_ERROR: 'Server error. Please try again later.',
  VALIDATION: 'Please check your input and try again.',
  GENERIC: 'Something went wrong. Please try again.'
};

// Success Messages
export const SUCCESS_MESSAGES = {
  PRODUCT_ADDED_TO_CART: 'Product added to cart successfully!',
  PRODUCT_ADDED_TO_WISHLIST: 'Product added to wishlist!',
  PRODUCT_REMOVED_FROM_WISHLIST: 'Product removed from wishlist',
  ORDER_PLACED: 'Your order has been placed successfully!',
  PROFILE_UPDATED: 'Profile updated successfully!',
  PASSWORD_CHANGED: 'Password changed successfully!'
};

// Feature Flags
export const FEATURE_FLAGS = {
  WISHLIST: true,
  REVIEWS: true,
  RECOMMENDATIONS: true,
  DARK_MODE: true,
  PWA: true,
  OFFLINE_MODE: false
};

// Social Media Links
export const SOCIAL_LINKS = {
  FACEBOOK: 'https://facebook.com',
  TWITTER: 'https://twitter.com',
  INSTAGRAM: 'https://instagram.com',
  LINKEDIN: 'https://linkedin.com'
};

// Contact Information
export const CONTACT_INFO = {
  EMAIL: 'support@store.com',
  PHONE: '+1 (555) 123-4567',
  ADDRESS: '123 Store Street, City, State 12345'
};

// Image Configuration
export const IMAGE_CONFIG = {
  PLACEHOLDER: '/placeholder.svg',
  QUALITY: 80,
  SIZES: {
    THUMBNAIL: { width: 150, height: 150 },
    SMALL: { width: 300, height: 300 },
    MEDIUM: { width: 600, height: 600 },
    LARGE: { width: 1200, height: 1200 }
  }
};

// SEO Configuration
export const SEO_CONFIG = {
  DEFAULT_TITLE: 'Store - Modern E-commerce Platform',
  TITLE_TEMPLATE: '%s | Store',
  DEFAULT_DESCRIPTION: 'Discover amazing products at great prices. Fast shipping, easy returns.',
  DEFAULT_IMAGE: '/og-image.jpg',
  SITE_URL: 'https://store.com'
};