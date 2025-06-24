# BestieAI - Emotional Support Companion

## Overview

BestieAI is a compassionate emotional support chatbot web application built with Flask. It provides personalized emotional support through empathetic responses, daily affirmations, and private journaling capabilities. The application features a warm, bestie-like personality using soft pastel aesthetics and caring language to create a safe space for users to express their feelings.

## System Architecture

### Frontend Architecture
- **Framework**: HTML5 with Bootstrap 5 for responsive design
- **Styling**: Custom CSS with soft pastel color scheme and gradients
- **JavaScript**: Vanilla JavaScript for form validation and UI enhancements
- **Design Philosophy**: Warm, caring, and accessible UI with "bestie" personality
- **Typography**: Google Fonts (Comfortaa for headings, Nunito for body text)

### Backend Architecture
- **Framework**: Python Flask with modular blueprint structure
- **Authentication**: Flask-Dance with Replit OAuth integration
- **Session Management**: Flask-Login for user session handling
- **Database ORM**: SQLAlchemy for database operations
- **WSGI Server**: Gunicorn for production deployment

### Data Storage Solutions
- **Primary Database**: PostgreSQL for user data and journal entries
- **Session Storage**: Server-side sessions with permanent session configuration
- **Authentication Storage**: OAuth tokens stored in database with user-browser session mapping

## Key Components

### Authentication System
- **Replit OAuth**: Secure authentication using Replit's OAuth service
- **User Management**: Automatic user creation and profile management
- **Session Handling**: Persistent sessions with browser session key tracking
- **Access Control**: Login required decorators for protected routes

### Emotional Support Engine
- **Emotion Recognition**: Predefined emotion categories with custom feeling support
- **Response Generation**: Contextual, empathetic responses based on user emotions
- **Personality**: Consistent "bestie" tone with caring, supportive language
- **Affirmations**: Mood-based daily affirmations for emotional wellness

### Journal System
- **Private Journaling**: Secure, user-specific journal entries
- **Auto-save**: Form persistence and data validation
- **Privacy**: User-isolated data storage with no cross-user access

## Data Flow

1. **User Authentication**: Users sign in via Replit OAuth, creating/updating user records
2. **Emotion Processing**: Users select emotions or input custom feelings
3. **Response Generation**: System maps emotions to appropriate supportive responses
4. **Journal Storage**: Private journal entries are saved to user-specific database records
5. **Affirmation Delivery**: Mood-based affirmations are generated and displayed

## External Dependencies

### Core Framework Dependencies
- **Flask 3.1.1**: Web application framework
- **Flask-SQLAlchemy 3.1.1**: Database ORM
- **Flask-Login 0.6.3**: User session management
- **Flask-Dance 7.1.0**: OAuth integration

### Database & Authentication
- **psycopg2-binary 2.9.10**: PostgreSQL adapter
- **PyJWT 2.10.1**: JWT token handling
- **oauthlib 3.3.1**: OAuth protocol implementation

### Production & Utilities
- **Gunicorn 23.0.0**: WSGI HTTP server
- **email-validator 2.2.0**: Email validation utilities

## Deployment Strategy

### Development Environment
- **Platform**: Replit with Nix package management
- **Database**: PostgreSQL via Replit services
- **Runtime**: Python 3.11 with automatic dependency management

### Production Deployment
- **WSGI Server**: Gunicorn with auto-scaling deployment target
- **Process Management**: Procfile configuration for platform deployment
- **Environment**: SSL/TLS support with proxy fix for secure connections
- **Port Configuration**: External port 80 mapped to internal port 5000

### Database Configuration
- **Connection Pooling**: Pre-ping enabled with 300-second recycle
- **Environment Variables**: DATABASE_URL for connection string
- **Schema Management**: Automatic table creation on application startup

## Changelog
- June 24, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.