# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a SvelteKit frontend for an e-commerce platform, built with Svelte 5, Tailwind CSS 4.0, and modern web development practices.

## Development Commands

### Setup & Development

```bash
# Install dependencies
npm install

# Start development server (http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Code Quality

```bash
# Run type checking
npm run check

# Run type checking in watch mode
npm run check:watch

# Run linting and formatting check
npm run lint

# Format code with Prettier
npm run format
```

### Testing

```bash
# Run E2E tests with Playwright
npm run test:e2e

# Run all tests (currently just E2E)
npm run test
```

## Architecture Overview

### Technology Stack

- **Framework**: SvelteKit with Svelte 5 (runes-based reactivity)
- **Styling**: Tailwind CSS 4.0 with custom design system
- **Build Tool**: Vite 7.0 with SvelteKit plugin
- **Testing**: Playwright for E2E testing
- **Type Checking**: JSDoc with svelte-check
- **Fonts**: Inter Variable and Outfit Variable from Fontsource

### Directory Structure

```
src/
├── lib/
│   ├── api/           # Backend API integration
│   ├── assets/        # Static assets (SVGs, images)
│   ├── components/    # Reusable UI components organized by domain
│   ├── stores/        # Global state management with Svelte 5 stores
│   └── utils/         # Utility functions and constants
├── routes/            # SvelteKit file-based routing
├── app.css           # Global Tailwind styles and custom CSS
└── app.html          # HTML shell template
```

### Component Architecture

Components are organized by domain:

- **`ui/`**: Base UI components (Button, Card, Badge, Drawer, etc.)
- **`layout/`**: Layout components (Header, navigation)
- **`product/`**: Product-specific components
- **`cart/`**: Shopping cart components
- **`checkout/`**: Checkout flow components
- **`home/`**: Homepage components

### State Management (Svelte 5 Runes)

The application uses Svelte 5's new runes-based reactivity system:

- **Auth Store**: User authentication state using `$state()` runes
- **Cart Store**: Shopping cart state management
- **Theme Store**: Dark/light theme preferences
- **Wishlist Store**: User wishlist functionality

All stores follow the context-based pattern with `setContext()` and `getContext()` for dependency injection.

### API Integration

Centralized API client (`src/lib/api/client.js`) with:
- JWT token management with automatic refresh
- Request/response interceptors
- Error handling with custom ApiError class
- Timeout handling and retry logic
- TypeScript-like JSDoc annotations

API modules by domain:
- `auth.js` - Authentication endpoints
- `products.js` - Product catalog
- `cart.js` - Shopping cart operations
- `orders.js` - Order management
- `reviews.js` - Product reviews

### Routing

SvelteKit file-based routing with:
- **`/`** - Homepage
- **`/products`** - Product catalog
- **`/products/[slug]`** - Product detail pages
- **`/cart`** - Shopping cart
- **`/checkout`** - Checkout flow
- **`/auth/login`** & **`/auth/register`** - Authentication
- **`/account/*`** - User account pages

## Key Patterns & Conventions

### Svelte 5 Runes Usage

The codebase uses Svelte 5's new reactivity system:

```javascript
// State management with $state()
class AuthStore {
  user = $state(null);
  isLoading = $state(true);
  isAuthenticated = $state(false);
  
  // Effects with $effect()
  constructor() {
    $effect(() => {
      this.init();
    });
  }
}

// Component props with $props()
let { children } = $props();
```

### Component Patterns

- Use `$props()` for component properties
- Implement `{@render children()}` for slot-like functionality
- Store instances created via context pattern in layout
- JSDoc comments for type safety without TypeScript

### API Client Pattern

All API calls go through the centralized client with:
- Automatic JWT token attachment
- Token refresh on 401 responses
- Request/response logging in development
- Consistent error handling

### Styling Conventions

- Tailwind CSS 4.0 with custom design system
- Dark mode support via CSS variables
- Component-scoped styles when needed
- Custom CSS properties for theme consistency

## Configuration Files

### Build Configuration

- **`vite.config.js`**: Vite configuration with SvelteKit plugin
- **`svelte.config.js`**: SvelteKit configuration with auto-adapter
- **`tailwind.config.js`**: Tailwind CSS configuration (if present)

### Development Tools

- **`playwright.config.js`**: E2E testing configuration
- **`jsconfig.json`**: JavaScript project configuration for VS Code
- **`.eslintrc.js`**: ESLint configuration with Svelte plugin
- **`.prettierrc`**: Prettier formatting rules

### Package Scripts

- `dev`: Start development server with hot reloading
- `build`: Build for production
- `preview`: Preview production build locally
- `check`: Run type checking with svelte-check
- `lint`: Check formatting and linting
- `format`: Auto-format code with Prettier
- `test:e2e`: Run Playwright E2E tests

## Development Notes

### Backend Integration

The frontend expects a Django REST API backend running on `http://localhost:8000/api/`. The API client is configured to:

- Handle JWT authentication with access/refresh tokens
- Automatically retry requests after token refresh
- Provide consistent error handling across all API calls

### State Persistence

- JWT tokens stored in localStorage
- Cart state persisted across sessions
- Theme preferences saved locally
- User preferences maintained in stores

### Performance Considerations

- SvelteKit provides SSR and client-side hydration
- Auto-adapter for deployment flexibility
- Vite for fast development and optimized builds
- Code splitting by routes automatically

### Testing Strategy

E2E testing with Playwright covers:
- User authentication flows
- Product browsing and search
- Shopping cart functionality
- Checkout processes
- Responsive behavior

Run tests against production build (`npm run build && npm run preview`) to ensure realistic testing conditions.