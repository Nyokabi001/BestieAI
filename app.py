import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Base class
class Base(DeclarativeBase):
    pass

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {'pool_pre_ping': True, "pool_recycle": 300}
db = SQLAlchemy(app, model_class=Base)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader
from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Session persistence
@app.before_request
def make_session_permanent():
    session.permanent = True

# EMOTION_RESPONSES and AFFIRMATIONS (your full dictionaries from before)
# ... (keep these as you had them) ...

# Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        display_name = current_user.first_name or current_user.email or "Bestie"
        return render_template('user_home.html', name=display_name, user=current_user)
    else:
        return render_template('landing.html')

@app.route('/chat')
@login_required
def chat():
    display_name = current_user.first_name or current_user.email or "Bestie"
    return render_template('chat.html', name=display_name, user=current_user)

@app.route('/respond', methods=['POST'])
@login_required
def respond():
    emotion = request.form.get('emotion', '').lower()
    custom_feeling = request.form.get('custom_feeling', '').strip()

    # Emotion mapping
    if custom_feeling:
        custom_lower = custom_feeling.lower()
        if any(w in custom_lower for w in ['tired', 'exhausted', 'drained']): emotion_key = 'tired'
        elif any(w in custom_lower for w in ['overwhelmed', 'too much']): emotion_key = 'overwhelmed'
        elif any(w in custom_lower for w in ['worried', 'scared']): emotion_key = 'anxious'
        elif any(w in custom_lower for w in ['frustrated', 'mad']): emotion_key = 'angry'
        elif any(w in custom_lower for w in ['down', 'hurt']): emotion_key = 'sad'
        elif any(w in custom_lower for w in ['alone', 'disconnected']): emotion_key = 'lonely'
        elif any(w in custom_lower for w in ['thrilled', 'pumped']): emotion_key = 'excited'
        elif any(w in custom_lower for w in ['good', 'great']): emotion_key = 'happy'
        else: emotion_key = 'confused'
        feeling_text = custom_feeling
    else:
        emotion_key = emotion if emotion in EMOTION_RESPONSES else 'confused'
        feeling_text = emotion

    import random
    response = random.choice(EMOTION_RESPONSES.get(emotion_key, EMOTION_RESPONSES['confused']))
    session['current_emotion'] = emotion_key

    display_name = current_user.first_name or current_user.email or "Bestie"
    return render_template('chat.html', name=display_name, feeling=feeling_text, response=response, user=current_user)

@app.route('/affirmation')
@login_required
def affirmation():
    emotion = session.get('current_emotion', 'happy')
    import random
    daily_affirmation = random.choice(AFFIRMATIONS.get(emotion, AFFIRMATIONS['happy']))

    display_name = current_user.first_name or current_user.email or "Bestie"
    return render_template('affirmation.html', name=display_name, affirmation=daily_affirmation, emotion=emotion, user=current_user)

@app.route('/journal')
@login_required
def journal():
    display_name = current_user.first_name or current_user.email or "Bestie"
    return render_template('journal.html', name=display_name, user=current_user)

@app.route('/save_journal', methods=['POST'])
@login_required
def save_journal():
    journal_entry = request.form.get('journal_entry', '').strip()

    if journal_entry:
        try:
            from models import JournalEntry
            new_entry = JournalEntry(user_id=current_user.id, content=journal_entry)
            db.session.add(new_entry)
            db.session.commit()
            flash('Your journal entry has been saved! 📝💕', 'success')
        except Exception as e:
            logging.error(f"Error saving journal entry: {e}")
            flash('There was a problem saving your entry. 😔', 'error')
    else:
        flash('Please write something before saving! ✨', 'info')

    return redirect(url_for('journal'))

# Auth routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in instead.')
            return redirect(url_for('login'))
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out.")
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    with app.app_context():
        import models  # Ensure models are loaded
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
