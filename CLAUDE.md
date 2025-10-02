# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack e-commerce platform consisting of:
- **Backend**: Django REST API with JWT authentication, user management, and e-commerce features
- **Frontend**: SvelteKit web application with modern UI components and state management
- **Database**: SQLite for development, PostgreSQL for production
- **Caching/Message Queue**: Redis for Celery task processing
- **Deployment**: Docker containerization ready

## Repository Structure

```
store/
├── back/                     # Django backend API
│   ├── accounts/            # User authentication & management
│   ├── base/               # Core e-commerce functionality
│   ├── back/               # Django project configuration
│   ├── templates/          # Email templates
│   ├── logs/               # Application logs
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies
│   └── CLAUDE.md          # Backend-specific documentation
├── front/                   # SvelteKit frontend application
│   ├── src/                # Frontend source code
│   │   ├── lib/            # Shared utilities, API clients, stores
│   │   ├── routes/         # SvelteKit routes and pages
│   │   ├── app.html        # HTML template
│   │   └── app.css         # Global styles
│   ├── static/             # Static assets
│   ├── package.json        # Node.js dependencies
│   ├── svelte.config.js    # SvelteKit configuration
│   ├── vite.config.js      # Vite build configuration
│   └── structure.md        # Frontend structure documentation
├── Pipfile                 # Pipenv configuration
├── docker-compose.yml     # Docker services configuration (corrected filename)
└── .env files             # Environment configurations
```

## Development Commands

### Environment Setup

Using Pipenv (recommended):
```bash
# Install pipenv if not installed
pip install pipenv

# Install dependencies and create virtual environment
pipenv install

# Activate virtual environment
pipenv shell

# Install development dependencies
pipenv install --dev
```

Using pip directly:
```bash
# Navigate to backend
cd back

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Frontend Development (SvelteKit)

```bash
# Navigate to frontend directory
cd front

# Install dependencies
npm install

# Start development server (default: http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting and formatting
npm run lint
npm run format

# Type checking with Svelte 5 + JSDoc
npm run check

# Run E2E tests
npm run test:e2e
```

### Docker Development

**Note**: The docker-compose file has a typo in the filename (`docker-comose.yml`) and uses incorrect app name `online_store` instead of `back` for Celery commands. Fix these before using Docker.

```bash
# After fixing filename and app name:
# Start all services (PostgreSQL, Redis, Django)
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build
```

### Database Operations

```bash
# Navigate to backend directory
cd back

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Reset database (SQLite only)
rm ../db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

### Development Server

```bash
cd back

# Run development server
python manage.py runserver

# Run with specific port
python manage.py runserver 8080

# Run with Docker (includes PostgreSQL and Redis)
docker-compose up web
```

### Testing

```bash
cd back

# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts
python manage.py test base

# Run specific test files
python test_api_endpoints.py
python test_auth_flow.py
python test_verification_model.py

# Run tests with Docker
docker-compose exec web python manage.py test
```

### Task Queue (Celery)

**Note**: Celery is configured in settings.py but not yet implemented. The celery.py file needs to be created at `back/back/celery.py` before these commands will work.

```bash
cd back

# After creating celery.py:
# Start Celery worker (requires Redis)
celery -A back worker -l info

# Start Celery beat scheduler
celery -A back beat -l info
```

### Full Stack Development

```bash
# Start backend (from project root)
cd back && python manage.py runserver

# Start frontend (from project root, in new terminal)
cd front && npm run dev

# Or start everything with Docker
docker-compose up
```

## Architecture Overview

### Backend Django Apps

**accounts app** - Complete user management system:
- Custom User model with UUID primary keys
- Role-based access control (customer, vendor, admin, superadmin)
- JWT authentication with refresh tokens and token blacklist
- Email verification with 6-digit codes (rate limited: 3 attempts per 30 min)
- Password reset with 6-digit codes and rate limiting
- Loyalty points system (gamification feature)
- User profiles with avatars, addresses, preferences, and cultural localization
- Login history tracking for security

**base app** - E-commerce core functionality:
- Product management with categories, variants, and stock tracking
- Shopping cart with session support
- Order processing and tracking
- Payment integration ready
- Review and rating system
- Wishlist functionality
- Coupon management system

**back project** - Django configuration:
- Environment-based settings using python-decouple
- JWT authentication with djangorestframework-simplejwt
- CORS configured for multiple Vite dev server ports (5173-5178)
- Database: SQLite (development), PostgreSQL ready (commented in settings)
- Redis and Celery configured (celery.py needs to be created)
- AWS S3 support ready (conditional on USE_S3 env var)
- Comprehensive logging to files (logs/django.log, logs/auth.log)
- Security headers and session configuration

### Frontend SvelteKit Architecture

**Frontend Structure**:
- **SvelteKit Framework**: Modern full-stack framework with SSR/SPA capabilities
- **Svelte 5 Runes**: New runes-based reactivity system (`$state`, `$derived`, `$effect`, `$props`)
- **Component Architecture**: Domain-organized UI components (ui/, layout/, product/, cart/, etc.)
- **State Management**: Svelte 5 stores with context-based dependency injection
- **Design System**: Tailwind CSS 4.0 with custom theme and premium patterns
- **Typography**: Variable fonts (Inter, Outfit) with advanced font features
- **API Integration**: Centralized client with JWT management and error handling
- **Type Safety**: JSDoc annotations for comprehensive type checking
- **Build System**: Vite 7.0 for fast development and optimized production builds
- **Testing**: Playwright for E2E testing, ESLint/Prettier for code quality

**Key Frontend Features**:
- Server-side rendering (SSR) and client-side navigation
- Progressive enhancement with SvelteKit
- Premium UI patterns (glass morphism, neumorphism, magnetic effects)
- Advanced animations with custom easing functions
- Dark/light theme with system preference detection
- Responsive design with mobile-first approach
- Shopping cart state management with persistence
- User authentication flow with JWT handling
- Product catalog with filtering and search
- Accessibility-first design (WCAG compliance)
- Performance optimizations (code splitting, lazy loading)
- E2E testing with Playwright

### Authentication Architecture

- **JWT-based authentication** using djangorestframework-simplejwt for API access
- **Email verification** with 6-digit codes and rate limiting (3 attempts per 30 min)
- **Password reset** with 6-digit codes and secure token handling
- **Role-based permissions** with custom user roles (customer, vendor, admin, superadmin)
- **Loyalty points system** for user engagement
- **Security features**: rate limiting, login history tracking

### API Structure

**Backend API** (Django REST Framework):
- Base URL: `http://localhost:8000/api/`
- **Authentication Endpoints** (`/api/accounts/`):
  - User registration, login, logout
  - Email verification workflows
  - Password reset functionality
  - Profile management
  - JWT token refresh
- **E-commerce Endpoints** (`/api/`):
  - Product CRUD with filtering and search
  - Category management
  - Shopping cart operations
  - Order processing
  - Review and wishlist management

**Frontend Routes** (SvelteKit):
- Base URL: `http://localhost:5173/`
- `/` - Home page
- `/products` - Product catalog
- `/products/[slug]` - Product detail pages
- `/cart` - Shopping cart
- `/checkout` - Checkout process
- `/auth/login` - User login
- `/auth/register` - User registration
- `/auth/verify-email` - Email verification
- `/auth/reset-password` - Password reset request
- `/auth/reset-password/confirm` - Password reset confirmation
- `/account` - User profile
- `/account/orders` - Order history
- `/account/wishlist` - User wishlist

### Database Design

- **UUID primary keys** for all models (security)
- **JSON fields** for flexible data (product specifications, user preferences)
- **Proper indexing** for performance optimization
- **Soft deletes** using is_active fields
- **Timestamp tracking** on all models

### Configuration Management

**Environment Files**:
- `.env` - Default configuration
- `.env.dev` - Development settings
- `.env.prod` - Production settings

**Required Environment Variables**:
```
SECRET_KEY=your-secret-key
DEBUG=True/False
ALLOWED_HOSTS=comma,separated,hosts
JWT_SECRET_KEY=jwt-signing-key
EMAIL_HOST_USER=smtp-username
EMAIL_HOST_PASSWORD=smtp-password
```

**Optional Variables** (for production):
- Database configuration (PostgreSQL)
- Redis configuration
- AWS S3 credentials
- Email backend settings

### Technology Stack

**Backend**:
- Django 5.2.5 + Django REST Framework 3.16.1
- JWT Authentication (djangorestframework-simplejwt)
- PostgreSQL (production) / SQLite (development)
- Redis + Celery for background tasks
- Pillow for image processing
- Gunicorn for production deployment

**Frontend**:
- SvelteKit (Svelte 5.0) with runes-based reactivity and JSDoc typing
- Tailwind CSS 4.0 with custom design system and premium UI patterns
- Vite 7.0 for build tooling and development server  
- Playwright for E2E testing
- ESLint + Prettier for code quality
- Variable fonts (Inter, Outfit) for premium typography
- Auto-adapter for deployment flexibility

**DevOps**:
- Docker + docker-compose for containerization
- Pipenv for Python dependency management
- npm for Node.js dependency management

## Key Features

### Advanced User Management
- Custom User model with comprehensive profile fields
- Email verification with 6-digit codes and rate limiting
- Password reset with 6-digit codes and secure handling
- Loyalty points system for user engagement
- Role-based access control (customer, vendor, admin, superadmin)
- Cultural localization support (preferred_language, preferred_currency)

### E-commerce Platform
- Product catalog with categories and variants
- Stock management and inventory tracking
- Shopping cart with persistence
- Order workflow with status tracking
- Payment gateway integration ready
- Review and rating system
- Wishlist and comparison features

### Developer Experience
- Test files included: test_api_endpoints.py, test_auth_flow.py, test_verification_model.py
- Docker configuration available (needs fixing: filename typo, wrong Celery app name)
- Comprehensive logging to files (django.log, auth.log)
- Environment-based configuration with python-decouple
- Hot reloading for both frontend and backend
- Modern frontend with SvelteKit (Svelte 5) and Vite 7
- E2E testing with Playwright
- Code quality tools: ESLint, Prettier, svelte-check

## Development Patterns

### Model Patterns
- UUID primary keys for security
- JSON fields for flexible attributes
- Soft deletes with is_active flags
- Timestamp fields on all models
- Custom managers for specialized creation

### API Patterns
- Generic API views (not ViewSets)
- Field `__all__` serialization pattern
- JWT authentication on all endpoints
- Pagination (20 items per page)
- Comprehensive filtering and search

### Security Patterns
- JWT tokens with refresh mechanism and blacklist
- Email verification with 6-digit codes (not JWT)
- Rate limiting on verification/reset (3 attempts per 30 min)
- Role-based permissions with custom decorators
- Password validation (8 char minimum, complexity requirements)
- Secure password reset with time-limited codes
- Security headers (XSS filter, content type nosniff, X-Frame-Options)

### Frontend Patterns
- **Svelte 5 Runes**: Use `$state()`, `$derived()`, `$effect()`, and `$props()` for reactivity
- **Component Architecture**: Domain-organized components (ui/, layout/, product/, cart/)
- **Context-Based Stores**: Use `setContext()` and `getContext()` for dependency injection
- **Server-Side Rendering**: SSR with SvelteKit for SEO and performance
- **API Client Pattern**: Centralized client with JWT token management and retry logic
- **Premium UI Patterns**: Glass morphism, neumorphism, magnetic effects, hover animations
- **Theme System**: CSS custom properties with dark/light mode support
- **Typography Scale**: Variable fonts with advanced OpenType features
- **Route-Based Code Splitting**: Automatic optimization through SvelteKit
- **Progressive Enhancement**: Accessibility-first development approach

## Testing Strategy

The project includes comprehensive test files:
- `test_api_endpoints.py` - API endpoint testing
- `test_auth_flow.py` - Authentication workflow testing
- `test_verification_model.py` - Email verification testing

**Backend Testing Approach**:
- Unit tests for all models and utilities
- API endpoint testing for all views
- Authentication flow testing
- Permission-based access testing
- Integration testing for complex workflows

**Frontend Testing Approach**:
- E2E testing with Playwright for critical user flows
- Component testing for UI components
- Integration testing for API communication
- Accessibility testing for WCAG compliance

## Deployment Notes

### Docker Deployment
The project includes a `docker-compose.yml` with:
- PostgreSQL database
- Redis for caching/queues
- Django web server
- Celery worker and beat scheduler

### Production Considerations
- Switch to PostgreSQL database
- Configure AWS S3 for media files
- Set up proper logging and monitoring
- Enable HTTPS and security headers
- Configure email backend for notifications
- Set up Celery for background tasks

## Common Tasks

### Adding New Backend Features
1. Create models in appropriate app (accounts or base)
2. Create serializers with `__all__` fields pattern
3. Create generic API views (not ViewSets)
4. Add URL patterns
5. Write comprehensive tests
6. Update permissions as needed

### Adding New Frontend Features
1. Create components using Svelte 5 runes (`$state`, `$props`, `$effect`, `$derived`)
2. Organize components by domain under `front/src/lib/components/` (ui/, layout/, product/, etc.)
3. Add routes in `front/src/routes/` following SvelteKit file-based conventions
4. Update API client in `front/src/lib/api/` if backend integration needed
5. Create context-based stores using `setContext()` and `getContext()` pattern
6. Apply Tailwind CSS 4.0 classes and custom design system tokens
7. Implement premium UI patterns (glass effects, animations, hover states)
8. Ensure dark/light theme compatibility with CSS custom properties
9. Write E2E tests for critical user flows with Playwright
10. Verify accessibility compliance and responsive design

### Database Schema Changes
1. Make model changes
2. Create migrations: `python manage.py makemigrations`
3. Review migration files
4. Apply migrations: `python manage.py migrate`
5. Test with existing data

### Testing New Code

**Backend Testing**:
1. Write unit tests for models
2. Write API tests for views
3. Test authentication flows
4. Run full test suite: `python manage.py test`
5. Test with Docker environment

**Frontend Testing**:
1. Write component tests for Svelte 5 runes-based components
2. Write E2E tests for user workflows: `npm run test:e2e`
3. Test API integration with JWT authentication flows
4. Run type checking with JSDoc annotations: `npm run check`
5. Verify responsiveness across device viewports
6. Test accessibility compliance (WCAG standards)
7. Validate dark/light theme functionality
8. Test premium UI interactions (hover effects, animations)
9. Performance testing with Lighthouse metrics

## File Locations

- **Backend code**: `back/` directory
- **Frontend code**: `front/` directory
- **Database**: `db.sqlite3` (SQLite, in project root)
- **Logs**: `logs/` directory (created by Django, in project root)
- **Email templates**: `back/templates/` directory (settings.py: BASE_DIR / 'templates')
- **Frontend static files**: `front/static/` directory
- **Environment files**: `.env`, `.env.dev`, `.env.prod` (project root)
- **Docker config**: `docker-comose.yml` (typo in filename, should be docker-compose.yml)
- **Python deps**: `requirements.txt` (current), `Pipfile` (outdated versions)

## Important Notes

### Development Environment
- Frontend development server runs on port 5173 (Vite 7.0 default)
- Backend development server runs on port 8000 (Django default)  
- Both can run simultaneously for full-stack development
- Hot module reloading enabled for both frontend and backend

### Technology Stack Integration
- **Svelte 5 Runes**: New reactivity system replaces traditional stores pattern
- **Tailwind CSS 4.0**: Uses `@theme` directive with CSS custom properties
- **Variable Fonts**: Inter Variable and Outfit Variable for premium typography
- **JSDoc Typing**: Comprehensive type safety without TypeScript overhead
- **Premium UI**: Glass morphism, neumorphism, and magnetic effects built-in
- **Dark Mode**: System preference detection with CSS custom properties
- **Performance**: Vite 7.0 with optimized build and development experience

### Known Issues to Fix
- **Docker Compose**: Filename typo `docker-comose.yml` → `docker-compose.yml`
- **Docker Compose**: Celery commands use wrong app name `online_store` → should be `back`
- **Celery**: Not implemented yet - need to create `back/back/celery.py`
- **Dependencies**: `Pipfile` has outdated versions - use `requirements.txt` instead
- **Templates**: Settings shows BASE_DIR (3 levels up) for templates path

### Deployment Readiness
- Frontend optimized with SvelteKit adapter-auto and Vite build pipeline
- Backend ready for PostgreSQL (commented config in settings.py)
- AWS S3 integration ready (conditional on USE_S3 env var)
- Gunicorn included for production WSGI server