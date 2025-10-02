# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django REST API backend for e-commerce platform with JWT authentication, role-based access control, and comprehensive user management. Uses Django 5.2.5 with DRF 3.16.1.

**Key Technologies**: Django REST Framework, JWT (simplejwt), PostgreSQL/SQLite, Redis (configured), Celery (needs implementation), python-decouple for config.

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies (requires requirements.txt to be created)
pip install -r requirements.txt
```

### Database Operations
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Reset database (SQLite)
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Run with specific port
python manage.py runserver 8080
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts
python manage.py test base

# Run specific test file
python manage.py test accounts.tests
```

### Shell and Utilities
```bash
# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Create app
python manage.py startapp [app_name]
```

## Project Architecture

### Apps Structure
- **accounts**: Custom user management, authentication, email verification, password reset
- **base**: Core e-commerce functionality (products, orders, cart, payments, reviews)
- **back**: Main Django project configuration

### Core Models Architecture

**User Management (accounts app)**:
- `User`: Custom user model with role-based permissions (customer, vendor, admin, superadmin)
- `EmailVerificationToken`: Email verification tokens with expiration
- `PasswordResetToken`: Secure password reset tokens
- `LoginHistory`: User login tracking and security

**E-commerce Core (base app)**:
- `Product`: Main product model with variants, images, and stock tracking
- `Category`: Hierarchical product categories
- `Brand`: Product brands
- `Cart/CartItem`: Shopping cart functionality
- `Order/OrderItem`: Order processing and tracking
- `Payment`: Payment processing with multiple gateways
- `Delivery`: Delivery tracking with location coordinates
- `Review`: Product reviews and ratings
- `Wishlist`: User wishlists
- `Coupon`: Discount coupons and promotions

### Authentication & Security
- **JWT Authentication**: Access/refresh tokens with blacklist (simplejwt)
- **Email Verification**: 6-digit codes with rate limiting (3 attempts per 30 min)
- **Password Reset**: 6-digit codes with time limits and rate limiting
- **Role-Based Access**: Custom permissions (customer, vendor, admin, superadmin)
- **Security Features**:
  - Rate limiting via Django cache
  - Login history tracking (IP, user agent)
  - Password validation (8 char min, complexity)
  - Security headers (XSS filter, nosniff, X-Frame-Options)

### API Structure
- Base URL: `http://localhost:8000/api/`
- Authentication endpoints: `/api/accounts/`
- E-commerce endpoints: `/api/`
- Uses Generic API views (not ViewSets as specified)
- Field `__all__` serialization pattern
- Comprehensive pagination (20 items per page)

### Database Design
- **Current**: SQLite (db.sqlite3 in project root)
- **Production Ready**: PostgreSQL config commented in settings.py
- **UUID Primary Keys**: All models use UUID for security
- **Indexing**: Optimized for queries on email, username, created_at
- **JSON Fields**: Flexible data (product specs, user preferences)
- **Soft Deletes**: is_active flags on models
- **Timestamps**: created_at, updated_at on all models

### Configuration
- **Environment**: python-decouple for .env file management
- **CORS**: Multiple Vite ports (5173-5178) + frontend URL
- **Redis**: Configured for Celery (localhost:6379)
- **Celery**: Settings ready, but celery.py not created yet
- **AWS S3**: Conditional support (USE_S3 env var)
- **Email**: Console backend (dev), SMTP ready (prod)
- **Logging**: File-based (logs/django.log, logs/auth.log)
- **Templates**: BASE_DIR / 'templates' (project root)

## Key Features

### User Management
- Custom User model (AbstractBaseUser + PermissionsMixin)
- UUID primary keys for all users
- Role-based access (customer, vendor, admin, superadmin)
- Email verification (6-digit codes, 30-min rate limit)
- Password reset (6-digit codes, time-limited)
- Loyalty points system (gamification)
- Profile fields: avatar, bio, addresses, preferences
- Cultural localization: preferred_language, preferred_currency

### E-commerce Features
- Product management with variants and images
- Hierarchical categories and brands
- Shopping cart with session support
- Complete order workflow
- Payment processing (multiple gateways)
- Delivery tracking with GPS coordinates
- Review and rating system
- Wishlist functionality
- Coupon management
- Stock tracking and management

### API Features
- **Authentication**: JWT with access/refresh tokens and blacklist
- **Pagination**: 20 items per page (PageNumberPagination)
- **Filtering**: django-filter integration on list views
- **Search**: SearchFilter and OrderingFilter enabled
- **Serialization**: Field `__all__` pattern, nested serializers
- **Error Handling**: Standardized responses via utils.create_response()
- **CORS**: Configured for multiple frontend ports

## Development Patterns

### Model Patterns
- UUID primary keys for security
- Soft deletes where appropriate (is_active fields)
- Created/updated timestamps on all models
- JSON fields for flexible attributes
- Proper model relationships with related_name
- Custom managers for user creation

### View Patterns
- **Generic Views**: ListCreateAPIView, RetrieveUpdateDestroyAPIView (not ViewSets)
- **Permissions**: IsAuthenticated as default, custom role-based decorators
- **Rate Limiting**: Implemented in utils.py (check_rate_limit function)
- **Response Format**: Standardized via utils.create_response()
  - Success: `{"status": "success", "data": {...}, "message": "..."}`
  - Error: `{"status": "error", "error": {...}, "error_code": "..."}`

### Serializer Patterns
- Field `__all__` serialization as specified
- Nested serializers for related objects
- Custom validation methods
- Read-only fields for computed properties
- Separate serializers for different operations when needed

## Environment Configuration

### Required Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated allowed hosts
- `JWT_SECRET_KEY`: JWT signing key
- `JWT_ACCESS_TOKEN_LIFETIME`: Access token lifetime (minutes)
- `JWT_REFRESH_TOKEN_LIFETIME`: Refresh token lifetime (minutes)
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password
- `FRONTEND_URL`: Frontend URL for CORS

### Optional Environment Variables
- **Database**: DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
- **Redis**: REDIS_HOST (default: localhost), REDIS_PORT (default: 6379)
- **AWS S3**: USE_S3, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
- **Email**: EMAIL_BACKEND, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, DEFAULT_FROM_EMAIL
- **Frontend**: FRONTEND_URL (for CORS), EMAIL_VERIFY_PATH, PASSWORD_RESET_PATH
- **App**: COMPANY_NAME (default: TechSavvy Store)

## Security Implementation

**Active Security Measures**:
- Rate limiting on email actions (utils.py: check_rate_limit)
- JWT token blacklist on logout
- Password validation (8 char min, complexity)
- Security headers (XSS filter, nosniff, X-Frame-Options)
- CORS whitelist (no wildcards)
- Email verification required for account activation

**Production Checklist**:
- Set DEBUG=False
- Use strong SECRET_KEY and JWT_SECRET_KEY
- Enable HTTPS and set secure cookie flags
- Configure real SMTP (not console backend)
- Enable PostgreSQL with strong credentials
- Regular dependency updates (pip-audit)

## Testing

**Test Files**:
- `test_api_endpoints.py` - API endpoint testing
- `test_auth_flow.py` - Authentication workflow testing
- `test_verification_model.py` - Email verification testing
- `final_test_demo.py` - Demonstration test suite

**Running Tests**:
```bash
# All tests
python manage.py test

# Specific app
python manage.py test accounts
python manage.py test base

# Specific test file
python test_auth_flow.py
```

**Test Coverage Areas**:
- User model and custom managers
- JWT authentication and refresh
- Email verification rate limiting
- Password reset workflows
- API endpoint permissions
- Serializer validation

## Important Implementation Notes

**Email Verification System**:
- Uses 6-digit random codes (not JWT tokens)
- Rate limiting: 3 attempts per 30 minutes
- Implemented in accounts/utils.py (send_email, check_rate_limit)
- Templates in back/templates/ directory

**Celery Status**:
- Redis and Celery configured in settings.py
- **Missing**: back/back/celery.py needs to be created
- Docker compose references wrong app name: "online_store" → should be "back"

**File Paths** (BASE_DIR = parent.parent.parent):
- Database: project_root/db.sqlite3
- Logs: project_root/logs/
- Templates: project_root/templates/ (not back/templates/)
- Media: project_root/media/

**Dependencies**:
- Use requirements.txt (current: Django 5.2.5, DRF 3.16.1)
- Pipfile is outdated (Django 5.0.1, DRF 3.14.0)