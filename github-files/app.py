import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import current_user

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    'pool_pre_ping': True,
    "pool_recycle": 300,
}

db = SQLAlchemy(app, model_class=Base)

# Create tables
with app.app_context():
    import models
    db.create_all()
    logging.info("Database tables created")

# Make session permanent
@app.before_request
def make_session_permanent():
    session.permanent = True

# Enhanced emotion-based responses with empathy and "bestie" language
EMOTION_RESPONSES = {
    'happy': [
        "Oh bestie, I'm literally glowing with you right now! Your happiness is like sunshine - it's warming my heart and making everything brighter. Keep shining, beautiful soul! 🌟💛",
        "Yesss bestie! I'm doing a little happy dance over here because your joy is absolutely contagious! Let's soak in this beautiful moment together and celebrate YOU! 🌈✨",
        "Sweet bestie, your happiness makes my whole day! I love seeing you light up like this. You deserve every single sparkle of joy that comes your way! 💫🦋"
    ],
    'sad': [
        "Oh honey, my heart is right there with you. It's okay to feel this sadness, bestie - you don't have to put on a brave face for me. I'm here to sit in this feeling with you for as long as you need. 💙🤗",
        "Bestie, I feel that heaviness with you. Sometimes sadness visits to teach us something or to help us heal. You're not alone in this - I'm wrapping you in the biggest virtual hug right now. 🌧️💕",
        "Sweet soul, your tears are sacred and your feelings are so valid. Take all the time you need, bestie. I'll be right here, holding space for your beautiful, tender heart. 🌸💗"
    ],
    'anxious': [
        "Oh bestie, I can feel that anxious energy with you. Let's breathe together, okay? You're safe right here, right now. That worried mind of yours is just trying to protect you, but you've got this, love. 🌊🕊️",
        "Sweet bestie, anxiety feels so scary, but you're braver than you know. Let's take this one gentle breath at a time. I'm not going anywhere - we'll get through this together. 🌿💜",
        "Honey, those anxious thoughts are loud, but they're not the truth about you. You're strong, you're capable, and right now, bestie, you're exactly where you need to be. Let's find some peace together. 🦋✨"
    ],
    'stressed': [
        "Oh bestie, I can feel how much you're carrying right now. That's a heavy load, love. You don't have to carry it all perfectly - just breathe and take it one small step at a time. You're doing amazing. 🌿💚",
        "Sweet soul, stress is your body's way of saying 'I need a moment.' Listen to it, bestie. You deserve rest, you deserve breaks, and you absolutely deserve to be gentle with yourself right now. ☁️💙",
        "Bestie, you're juggling so much and that takes incredible strength. But even the strongest people need to pause and breathe. Let's find some calm in this storm together, okay? 🌱🤍"
    ],
    'angry': [
        "Bestie, I feel that fire in you, and it's okay. Your anger is telling you something important - maybe that a boundary was crossed or something feels unfair. Let's honor that feeling and find a way to channel it gently. 🔥➡️🌊",
        "Oh honey, that anger is so valid. You have every right to feel upset, bestie. Let's sit with this energy for a moment and then see how we can transform it into something that serves you better. You're not bad for feeling this way. ⚡💗",
        "Sweet bestie, anger can be such a powerful teacher. It shows us where we need protection or change. Take some deep breaths with me - let's honor this feeling and then decide what to do with all that fierce energy. 🌋➡️🌸"
    ],
    'lonely': [
        "Oh bestie, loneliness is one of the hardest feelings, but you're not alone anymore. I'm right here with you, and I want you to know that your presence in this world matters so much. You are seen, you are valued, and you are loved. 🌙💫",
        "Sweet soul, I feel that ache with you. Loneliness whispers lies about our worth, but bestie, you are precious beyond measure. Even when the world feels empty, you have me, and there are others who care about you too. 🌻💛",
        "Bestie, that lonely feeling is so real and so hard. But you reaching out to me right now? That's courage, love. You're not as alone as you feel - your heart is connected to mine and to so many others who care. 🌸🤗"
    ],
    'excited': [
        "BESTIE! I am literally bouncing with excitement for you right now! That spark in you is absolutely magical - let's channel all this beautiful energy into something amazing together! ✨🎉",
        "Oh my gosh, bestie, your excitement is giving me LIFE! I can feel your energy radiating through the screen and it's making me so happy! Let's ride this wave of joy and see where it takes us! 🌈⚡",
        "YES YES YES, bestie! This is what I love to see - you all lit up and excited! Your enthusiasm is like fireworks in my heart. Let's turn this beautiful energy into something wonderful! 💫🎆"
    ],
    'confused': [
        "Oh bestie, confusion is actually a beautiful place to be - it means you're growing and your heart is asking important questions. There's no rush to figure it all out right now, love. Let's sit in this uncertainty together and trust that clarity will come. 🌙🔮",
        "Sweet bestie, not knowing feels uncomfortable, but it's also where all the magic happens. You're in the space between who you were and who you're becoming. That's sacred ground, love. Take your time. 🌱✨",
        "Bestie, your confused heart is actually really wise - it's telling you to slow down and really feel into what's right for you. There's no wrong answer here, just your beautiful, unfolding truth. I believe in your inner knowing. 🦋🌸"
    ],
    'overwhelmed': [
        "Oh sweet bestie, I can feel how much you're holding right now. It's like trying to carry water in your hands, isn't it? Let's put some of that down together. You don't have to do it all at once, love. One breath, one step, one moment. 🌊💙",
        "Bestie, overwhelm is your soul saying 'this is too much right now.' And that's okay! You're human, not a machine. Let's break this down into tiny, manageable pieces. You've got this, but you don't have to do it all today. 🌿🤍",
        "Sweet soul, when everything feels like too much, remember this: you've survived 100% of your hardest days so far. You're stronger than you know, bestie, but strength also means knowing when to rest and regroup. 🌸💚"
    ],
    'tired': [
        "Oh bestie, I can feel that bone-deep tiredness. You've been running on empty, haven't you? Rest isn't weakness, love - it's wisdom. Your tired soul is asking for exactly what it needs. Let's honor that together. 🌙💜",
        "Sweet bestie, exhaustion is your body's way of saying 'I've given all I can give right now.' That's not failure - that's being beautifully, perfectly human. You deserve to rest without guilt, love. 🌸😴",
        "Bestie, you've been carrying so much for so long. Of course you're tired! That tired feeling isn't something to push through - it's an invitation to be gentle with yourself. You deserve care, especially from yourself. ☁️💤"
    ]
}

# Enhanced affirmations with more warmth and "bestie" energy
AFFIRMATIONS = {
    'happy': [
        "Bestie, your joy is a superpower that lights up every room you enter. Keep shining your beautiful light!",
        "You radiate happiness like sunshine, and the world is brighter because you're in it, bestie.",
        "Your smile is medicine for this world. Never underestimate the magic you bring, beautiful soul."
    ],
    'sad': [
        "Bestie, your tender heart that feels so deeply is actually your greatest strength. Honor those tears - they're healing you.",
        "Even in sadness, you are worthy of love, care, and gentle kindness. Take all the time you need, sweet soul.",
        "Your feelings are sacred, bestie. Let yourself feel it all - you're braver than you know for facing this with an open heart."
    ],
    'anxious': [
        "Bestie, you are safe in this moment. Your worried heart just wants to protect you, but you've got this, love.",
        "Anxiety whispers lies, but your truth is this: you are capable, you are loved, and you will find your way through.",
        "Sweet bestie, breathe with me. In this moment, you have everything you need. Trust your beautiful, resilient heart."
    ],
    'stressed': [
        "Bestie, you don't have to carry the world on your shoulders. You're doing amazingly well with what you have.",
        "Stress is just energy that needs direction. You're stronger than you know and worthy of rest, sweet soul.",
        "Take it one breath at a time, bestie. You've survived every hard day so far - this one is no different."
    ],
    'angry': [
        "Your anger is information, bestie. It's showing you where your boundaries need to be stronger. Honor that wisdom.",
        "That fire in you can fuel change and growth. You're allowed to feel angry - now let's channel it with love.",
        "Bestie, your anger is valid and powerful. Use it to protect what matters most, including your beautiful heart."
    ],
    'lonely': [
        "You are never truly alone, bestie. You carry love within you and you are deeply cherished by those who truly see you.",
        "Loneliness is just love with nowhere to go. You are worthy of connection and belonging, sweet soul.",
        "Your heart that feels lonely is the same heart that loves deeply. You belong, bestie - never doubt that."
    ],
    'excited': [
        "Your excitement is contagious magic, bestie! That spark in you can light up the whole world when you let it shine.",
        "Yes, bestie! That energy you're feeling is pure life force. Trust it, follow it, and watch miracles unfold.",
        "Your enthusiasm is a gift to everyone around you. Never dim that beautiful light - the world needs your spark!"
    ],
    'confused': [
        "Not knowing is actually sacred space, bestie. You're exactly where you need to be in your beautiful unfolding.",
        "Confusion means you're growing beyond who you used to be. Trust the process, sweet soul - clarity is coming.",
        "Your confused heart is actually incredibly wise, bestie. It's asking all the right questions for your highest good."
    ],
    'overwhelmed': [
        "You're carrying so much with such grace, bestie. It's okay to put some things down and just breathe for a moment.",
        "Overwhelm means you care deeply about many things. That beautiful heart of yours just needs some gentle tending.",
        "One thing at a time, sweet bestie. You don't have to solve everything today - just this moment is enough."
    ],
    'tired': [
        "Rest is not a reward for completed work, bestie - it's a basic need for your beautiful, human soul.",
        "Your tiredness is wisdom speaking. Listen to it with love and give yourself the care you so freely give others.",
        "Being tired doesn't make you weak, bestie. It makes you human. Honor your need for rest without guilt."
    ]
}

@app.route('/')
def home():
    if current_user.is_authenticated:
        display_name = current_user.first_name or current_user.email or "Bestie"
        return render_template('user_home.html', name=display_name, user=current_user)
    else:
        return render_template('landing.html')

@app.route('/chat')
def chat():
    display_name = current_user.first_name or current_user.email or "Bestie"
    return render_template('chat.html', name=display_name, user=current_user)

@app.route('/respond', methods=['POST'])
def respond():
    emotion = request.form.get('emotion', '').lower()
    custom_feeling = request.form.get('custom_feeling', '').strip()
    
    if custom_feeling:
        custom_lower = custom_feeling.lower()
        if any(word in custom_lower for word in ['tired', 'exhausted', 'drained', 'worn out']):
            emotion_key = 'tired'
        elif any(word in custom_lower for word in ['overwhelmed', 'too much', 'can\'t handle', 'drowning']):
            emotion_key = 'overwhelmed'
        elif any(word in custom_lower for word in ['worried', 'nervous', 'scared', 'fearful']):
            emotion_key = 'anxious'
        elif any(word in custom_lower for word in ['frustrated', 'mad', 'annoyed', 'irritated']):
            emotion_key = 'angry'
        elif any(word in custom_lower for word in ['down', 'depressed', 'blue', 'heartbroken', 'hurt']):
            emotion_key = 'sad'
        elif any(word in custom_lower for word in ['alone', 'isolated', 'disconnected', 'empty']):
            emotion_key = 'lonely'
        elif any(word in custom_lower for word in ['thrilled', 'pumped', 'energized', 'enthusiastic']):
            emotion_key = 'excited'
        elif any(word in custom_lower for word in ['good', 'great', 'wonderful', 'amazing', 'fantastic']):
            emotion_key = 'happy'
        else:
            emotion_key = 'confused'
        feeling_text = custom_feeling
    else:
        emotion_key = emotion if emotion in EMOTION_RESPONSES else 'confused'
        feeling_text = emotion
    
    import random
    response = random.choice(EMOTION_RESPONSES.get(emotion_key, EMOTION_RESPONSES['confused']))
    session['current_emotion'] = emotion_key
    
    display_name = current_user.first_name or current_user.email or "Bestie"
    return render_template('chat.html', 
                         name=display_name, 
                         feeling=feeling_text, 
                         response=response,
                         user=current_user)

@app.route('/affirmation')
def affirmation():
    emotion = session.get('current_emotion', 'happy')
    
    import random
    daily_affirmation = random.choice(AFFIRMATIONS.get(emotion, AFFIRMATIONS['happy']))
    
    display_name = current_user.first_name or current_user.email or "Bestie"
    return render_template('affirmation.html', 
                         name=display_name, 
                         affirmation=daily_affirmation,
                         emotion=emotion,
                         user=current_user)

@app.route('/journal')
def journal():
    display_name = current_user.first_name or current_user.email or "Bestie"
    return render_template('journal.html', name=display_name, user=current_user)

@app.route('/save_journal', methods=['POST'])
def save_journal():
    journal_entry = request.form.get('journal_entry', '').strip()
    
    if journal_entry:
        try:
            from models import JournalEntry
            new_entry = JournalEntry(
                user_id=current_user.id,
                content=journal_entry
            )
            db.session.add(new_entry)
            db.session.commit()
            
            flash('Your journal entry has been saved! Thank you for sharing with me. 📝💕', 'success')
        except Exception as e:
            logging.error(f"Error saving journal entry: {e}")
            flash('Sorry, there was an issue saving your entry. Please try again! 😔', 'error')
    else:
        flash('Please write something before saving your journal entry! ✨', 'info')
    
    return redirect(url_for('journal'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)