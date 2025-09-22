# Medical API Project

## Overview

This is a FastAPI-based Medical Practice Management system designed for doctor registration, authentication, and profile management. The application provides a RESTful API for medical professionals to register, verify their accounts through OTP, manage their profiles, and access master data for medical specialities and sub-specialities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs with automatic API documentation
- **SQLAlchemy**: ORM for database operations with declarative base models
- **Alembic**: Database migration management (configured but migrations not visible in current structure)

### Authentication & Security
- **JWT (JSON Web Tokens)**: Stateless authentication using python-jose library
- **Password Hashing**: Secure password storage using bcrypt via passlib
- **Bearer Token Authentication**: HTTP Bearer scheme for API endpoint protection
- **OTP Verification**: Email-based one-time password system for account verification

### Database Design
- **PostgreSQL**: Primary database using psycopg2-binary driver
- **Connection Pooling**: Configured with pool_pre_ping and pool_recycle for reliability
- **Five main entities**:
  - **Doctor**: Core user entity with profile information and medical credentials
  - **MedicalSpeciality**: Master data for medical specializations
  - **MedicalSubSpeciality**: Hierarchical sub-specializations linked to main specialities
  - **SocialAccount**: Social media platform connections for doctors with OAuth tokens
  - **Post**: Scheduled social media posts with content, timing, and status tracking

### API Structure
- **Modular Router Design**: Separate routers for different functional areas
  - `/auth`: Registration, login, and OTP verification endpoints
  - `/doctor`: Doctor profile management (get/update profile)
  - `/master`: Master data endpoints for specialities and sub-specialities
  - `/social`: Social media account connection and OAuth management
  - `/posts`: Post scheduling, management, and CRUD operations
- **Pydantic Schemas**: Request/response validation and serialization
- **Dependency Injection**: Database sessions and authentication handled via FastAPI dependencies

### Social Media Scheduler
- **Platform Support**: Facebook, Instagram, LinkedIn, Twitter, YouTube, Reddit, Quora
- **OAuth Integration**: Ready-to-implement OAuth2 flows for platform connections
- **Post Scheduling**: Create, update, and cancel scheduled posts with timezone-aware handling
- **Background Processing**: APScheduler runs every minute to publish due posts
- **Publisher Pattern**: Extensible publisher classes for each platform with common interface
- **Status Tracking**: Post status progression (scheduled → published/failed) with error logging

### Configuration Management
- **Environment-based Settings**: Database URL, JWT secrets, and other sensitive data via environment variables
- **Centralized Configuration**: Settings class with validation and defaults
- **Security Validation**: Enforced requirements for critical environment variables

### Data Validation & Serialization
- **Pydantic Models**: Type-safe request/response handling with email validation
- **Separation of Concerns**: Distinct schemas for create, update, and response operations
- **Automatic Documentation**: OpenAPI/Swagger documentation generation

## External Dependencies

### Core Framework Dependencies
- **FastAPI**: Web framework with automatic API documentation
- **Uvicorn**: ASGI server for running the FastAPI application
- **SQLAlchemy**: Database ORM for PostgreSQL operations
- **Pydantic**: Data validation and serialization with email support

### Security & Authentication
- **python-jose[cryptography]**: JWT token creation and verification
- **passlib[bcrypt]**: Password hashing and verification

### Database Integration
- **PostgreSQL**: Primary database system (requires DATABASE_URL environment variable)
- **psycopg2-binary**: PostgreSQL adapter for Python
- **Alembic**: Database migration management

### Email & Communication
- **OTP System**: Custom implementation for email verification (email sending functionality referenced but not implemented in visible code)

### Environment Requirements
- **DATABASE_URL**: PostgreSQL connection string
- **SESSION_SECRET**: JWT signing secret key
- **DEBUG**: Optional debug mode flag