# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django REST API e-commerce backend built with Django REST Framework. The project implements a complete e-commerce system with user management, product catalog, shopping cart, orders, payments, and delivery tracking.

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
- JWT authentication with refresh tokens using `rest_framework_simplejwt`
- Role-based permissions (Customer, Vendor, Admin, SuperAdmin)
- Email verification system with secure tokens
- Password reset with secure tokens and tracking
- Login history tracking with IP and user agent
- Account locking after failed login attempts
- Two-factor authentication ready

### API Structure
- Base URL: `http://localhost:8000/api/`
- Authentication endpoints: `/api/accounts/`
- E-commerce endpoints: `/api/`
- Uses Generic API views (not ViewSets as specified)
- Field `__all__` serialization pattern
- Comprehensive pagination (20 items per page)

### Database Design
- PostgreSQL ready (configured but SQLite active for development)
- UUID primary keys for all models
- Proper indexing for performance
- JSON fields for flexible data storage (features, specifications, attributes)
- Follows second normal form design principles

### Configuration
- Environment-based configuration using `python-decouple`
- Separate settings for development/production
- Redis configured for Celery (task queue)
- AWS S3 support for file storage (optional)
- CORS configured for frontend integration
- Email backend configured for notifications

## Key Features

### User Management
- Custom user model with profile fields
- Role-based access control
- Email verification workflow
- Secure password reset
- Login history and security tracking
- Account lockout protection

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
- JWT authentication with refresh tokens
- Comprehensive filtering and search
- Pagination on all list endpoints
- Nested serialization for related objects
- Error handling and validation
- CORS support for frontend integration

## Development Patterns

### Model Patterns
- UUID primary keys for security
- Soft deletes where appropriate (is_active fields)
- Created/updated timestamps on all models
- JSON fields for flexible attributes
- Proper model relationships with related_name
- Custom managers for user creation

### View Patterns
- Generic API views (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
- Permission classes for role-based access
- Custom authentication classes
- Filtering and search capabilities
- Proper error handling and responses

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
- Database configuration (PostgreSQL)
- Redis configuration (Celery)
- AWS S3 configuration
- Email backend settings

## Security Considerations
- Never commit sensitive environment variables
- Use secure JWT secret keys
- Implement proper CORS settings
- Validate all user inputs
- Use HTTPS in production
- Implement rate limiting for authentication endpoints
- Regular security audits of dependencies

## Testing Strategy
- Unit tests for all models
- API endpoint testing
- Authentication flow testing
- Permission testing
- Integration testing for complex workflows
- Test data factories for consistent testing