# BestieAI - Your Emotional Support Companion 💕

BestieAI is an empathetic emotional support chatbot web application built with Flask. It provides personalized, caring responses based on user emotions, daily affirmations, and private journaling functionality with a warm, "bestie" personality.

## Features

- **Emotional Support Chat**: Share your feelings and receive personalized, empathetic responses
- **Daily Affirmations**: Get uplifting affirmations tailored to your current emotional state
- **Personal Journal**: Private, secure journaling space with auto-save functionality
- **User Authentication**: Secure sign-in with Replit authentication
- **Responsive Design**: Beautiful, soft pastel UI that works on all devices
- **Intelligent Emotion Mapping**: Recognizes custom feelings and maps them to appropriate responses

## Tech Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL with SQLAlchemy
- **Authentication**: Flask-Dance with Replit OAuth
- **Frontend**: Bootstrap 5, Custom CSS, Vanilla JavaScript
- **Deployment**: Gunicorn WSGI server

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bestie-ai.git
cd bestie-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DATABASE_URL="your-postgresql-url"
export SESSION_SECRET="your-secret-key"
export REPL_ID="your-replit-id"  # For Replit authentication
```

4. Run the application:
```bash
python main.py
```

## Deployment

### Heroku Deployment

1. Create a new Heroku app
2. Add PostgreSQL addon
3. Set environment variables in Heroku config
4. Deploy using Git:

```bash
git add .
git commit -m "Deploy BestieAI"
git push heroku main
```

### Other Platforms

The app includes a `Procfile` for easy deployment to platforms like Railway, Render, or DigitalOcean App Platform.

## Environment Variables

- `DATABASE_URL`: PostgreSQL database connection string
- `SESSION_SECRET`: Secret key for Flask sessions
- `REPL_ID`: Replit application ID for authentication
- `ISSUER_URL`: OAuth issuer URL (defaults to Replit's OIDC)

## Project Structure

- `app.py`: Main Flask application with routes and emotion responses
- `models.py`: Database models for users, OAuth, and journal entries
- `replit_auth.py`: Authentication system using Replit OAuth
- `templates/`: HTML templates with Jinja2
- `static/`: CSS and JavaScript files
- `main.py`: Application entry point

## Features in Detail

### Emotion Support System
- 10 different emotional states with multiple response variations
- Custom feeling input with intelligent mapping
- Personalized responses using "bestie" language
- Session-based emotion tracking for affirmations

### Journaling System
- Auto-save drafts in localStorage
- Word count tracking
- Auto-resizing textarea
- Private, secure storage per user

### Design Philosophy
- Soft pastel color scheme (pinks and creams)
- Rounded, comfortable fonts (Comfortaa & Nunito)
- Accessible design with keyboard navigation
- Mobile-first responsive layout

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you need help or have questions, please open an issue on GitHub or contact the maintainers.

---

Made with 💕 for emotional wellness and mental health support.