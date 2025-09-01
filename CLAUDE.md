# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack e-commerce platform consisting of:
- **Backend**: Django REST API with JWT authentication, user management, and e-commerce features
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
├── Pipfile                 # Pipenv configuration
├── docker-compose.yml     # Docker services configuration
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

### Docker Development

```bash
# Start all services (PostgreSQL, Redis, Django, Celery)
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

```bash
cd back

# Start Celery worker (requires Redis)
celery -A back worker -l info

# Start Celery beat scheduler
celery -A back beat -l info

# With Docker (automatic startup)
docker-compose up celery
docker-compose up celery-beat
```

## Architecture Overview

### Backend Django Apps

**accounts app** - Complete user management system:
- Custom User model with UUID primary keys
- Role-based access control (customer, vendor, admin, superadmin)
- JWT authentication with refresh tokens
- Email verification with gamification (loyalty points system)
- Password reset with secure token handling
- User profiles with avatars, addresses, and preferences

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
- JWT authentication setup
- CORS configuration for frontend integration
- Database configuration (SQLite dev, PostgreSQL prod)
- Celery integration for background tasks
- AWS S3 support for file storage

### Authentication Architecture

- **JWT-based authentication** using djangorestframework-simplejwt
- **Stateless email verification** with JWT tokens (6 token types)
- **Role-based permissions** with custom user roles
- **Gamification system** with loyalty points and achievements
- **Security features**: account lockout, login history, two-factor ready

### API Structure

Base URL: `http://localhost:8000/api/`

**Authentication Endpoints** (`/api/accounts/`):
- User registration, login, logout
- Email verification workflows
- Password reset functionality
- Profile management
- JWT token refresh

**E-commerce Endpoints** (`/api/`):
- Product CRUD with filtering and search
- Category management
- Shopping cart operations
- Order processing
- Review and wishlist management

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

## Key Features

### Advanced User Management
- Custom User model with comprehensive profile fields
- Progressive registration with gamification
- JWT-based email verification (stateless)
- Loyalty points system with achievements
- Role-based access control
- Cultural localization support

### E-commerce Platform
- Product catalog with categories and variants
- Stock management and inventory tracking
- Shopping cart with persistence
- Order workflow with status tracking
- Payment gateway integration ready
- Review and rating system
- Wishlist and comparison features

### Developer Experience
- Comprehensive test suite with custom test cases
- Docker containerization for consistent environments
- Detailed logging system
- API documentation ready
- Environment-based configuration
- Background task processing with Celery

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
- JWT tokens with refresh mechanism
- Email verification before account activation
- Role-based permissions
- Input validation and sanitization
- Secure password reset flows

## Testing Strategy

The project includes comprehensive test files:
- `test_api_endpoints.py` - API endpoint testing
- `test_auth_flow.py` - Authentication workflow testing
- `test_verification_model.py` - Email verification testing

**Testing Approach**:
- Unit tests for all models and utilities
- API endpoint testing for all views
- Authentication flow testing
- Permission-based access testing
- Integration testing for complex workflows

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

### Adding New Features
1. Create models in appropriate app (accounts or base)
2. Create serializers with `__all__` fields pattern
3. Create generic API views (not ViewSets)
4. Add URL patterns
5. Write comprehensive tests
6. Update permissions as needed

### Database Schema Changes
1. Make model changes
2. Create migrations: `python manage.py makemigrations`
3. Review migration files
4. Apply migrations: `python manage.py migrate`
5. Test with existing data

### Testing New Code
1. Write unit tests for models
2. Write API tests for views
3. Test authentication flows
4. Run full test suite: `python manage.py test`
5. Test with Docker environment

## File Locations

- **Backend code**: `back/` directory
- **Database**: `db.sqlite3` (development)
- **Logs**: `back/logs/` directory
- **Templates**: `back/templates/` directory
- **Static files**: Configured for Django static files
- **Environment files**: `.env*` files in root