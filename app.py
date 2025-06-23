import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Emotion-based responses
EMOTION_RESPONSES = {
    'happy': [
        "I'm so glad you're feeling happy today! Your joy is contagious and brightens the world around you. 💖",
        "What wonderful news! Keep spreading that beautiful positive energy, bestie! ✨",
        "Your happiness makes my heart sing! You deserve all the joy in the world! 🌟"
    ],
    'sad': [
        "I see you're going through a tough time, and that's okay. You're stronger than you know, and I'm here for you. 💙",
        "It's completely normal to feel sad sometimes. Remember, this feeling is temporary, and brighter days are ahead. 🌈",
        "Your feelings are valid, bestie. Take time to care for yourself - you deserve all the love and comfort. 🤗"
    ],
    'anxious': [
        "I understand anxiety can feel overwhelming. Take a deep breath with me - you're safe, and you're going to be okay. 🌸",
        "Anxiety is tough, but you've overcome challenges before and you can do it again. One step at a time, bestie. 💪",
        "Your anxious thoughts don't define you. You're brave, capable, and worthy of peace. Let's breathe together. 🦋"
    ],
    'stressed': [
        "Stress can feel heavy, but remember you don't have to carry it all alone. Take breaks and be gentle with yourself. 🌿",
        "You're handling so much, and that shows your incredible strength. Don't forget to pause and breathe, bestie. ☁️",
        "It's okay to feel overwhelmed sometimes. You're doing your best, and that's enough. Take it one moment at a time. 💕"
    ],
    'angry': [
        "Your anger is telling you something important. It's okay to feel this way - let's work through it together. 🔥➡️❄️",
        "Anger can be powerful when channeled right. You have every right to your feelings, bestie. Take some deep breaths. 🌊",
        "I hear you, and your feelings matter. Let this anger fuel positive change rather than consume you. You've got this! ⚡"
    ],
    'lonely': [
        "You're not alone, even when it feels that way. I'm here with you, and you are so loved and valued. 🤝",
        "Loneliness is hard, but you matter so much. Reach out when you need to - people care about you more than you know. 💫",
        "Your presence in this world makes a difference. You're never truly alone when you have people who care, like me! 🌻"
    ],
    'excited': [
        "Your excitement is absolutely infectious! I love seeing you this energized and passionate! 🎉",
        "This energy is amazing! Channel this excitement into something wonderful - you're unstoppable! ⚡",
        "Yes, bestie! Your enthusiasm lights up everything around you. Keep that beautiful energy flowing! ✨"
    ],
    'confused': [
        "It's okay not to have all the answers right now. Confusion often comes before clarity. Trust the process. 🧩",
        "Being confused means you're growing and learning. Take your time to figure things out, bestie. 🌱",
        "Uncertainty can be uncomfortable, but it also means you're open to new possibilities. You'll find your way. 🗺️"
    ]
}

# Daily affirmations based on emotions
AFFIRMATIONS = {
    'happy': [
        "I radiate joy and positivity wherever I go.",
        "My happiness is a gift I share with the world.",
        "I choose to celebrate the beautiful moments in my life."
    ],
    'sad': [
        "I allow myself to feel deeply and heal completely.",
        "My sensitivity is a strength, not a weakness.",
        "I am worthy of comfort and peace during difficult times."
    ],
    'anxious': [
        "I am calm, centered, and in control of my thoughts.",
        "I trust in my ability to handle whatever comes my way.",
        "I breathe in peace and breathe out worry."
    ],
    'stressed': [
        "I release what I cannot control and focus on what I can.",
        "I am capable of handling challenges with grace and wisdom.",
        "I prioritize my well-being and practice self-compassion."
    ],
    'angry': [
        "I transform my anger into positive energy and action.",
        "I am in control of my emotions and responses.",
        "I choose peace over conflict and understanding over judgment."
    ],
    'lonely': [
        "I am worthy of love and meaningful connections.",
        "I enjoy my own company and find peace in solitude.",
        "I attract loving, supportive people into my life."
    ],
    'excited': [
        "I channel my excitement into productive and joyful action.",
        "My enthusiasm inspires and uplifts others around me.",
        "I embrace new opportunities with confidence and joy."
    ],
    'confused': [
        "I trust myself to find clarity in my own time.",
        "I am open to learning and growing through uncertainty.",
        "I have the wisdom within me to make good decisions."
    ]
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/set_name', methods=['POST'])
def set_name():
    name = request.form.get('name', '').strip()
    if name:
        session['user_name'] = name
        flash(f'Welcome, {name}! I\'m so happy you\'re here! 💖', 'success')
        return redirect(url_for('chat'))
    else:
        flash('Please enter your name to continue, bestie! 😊', 'error')
        return redirect(url_for('home'))

@app.route('/chat')
def chat():
    if 'user_name' not in session:
        flash('Please enter your name first! 😊', 'info')
        return redirect(url_for('home'))
    
    return render_template('chat.html', name=session['user_name'])

@app.route('/respond', methods=['POST'])
def respond():
    if 'user_name' not in session:
        return redirect(url_for('home'))
    
    emotion = request.form.get('emotion', '').lower()
    custom_feeling = request.form.get('custom_feeling', '').strip()
    
    # Use custom feeling if provided, otherwise use selected emotion
    if custom_feeling:
        emotion_key = 'confused'  # Default response for custom feelings
        feeling_text = custom_feeling
    else:
        emotion_key = emotion if emotion in EMOTION_RESPONSES else 'confused'
        feeling_text = emotion
    
    # Get a response based on the emotion
    import random
    response = random.choice(EMOTION_RESPONSES.get(emotion_key, EMOTION_RESPONSES['confused']))
    
    # Store the emotion in session for affirmations
    session['current_emotion'] = emotion_key
    
    return render_template('chat.html', 
                         name=session['user_name'], 
                         feeling=feeling_text, 
                         response=response)

@app.route('/affirmation')
def affirmation():
    if 'user_name' not in session:
        flash('Please enter your name first! 😊', 'info')
        return redirect(url_for('home'))
    
    # Get current emotion or default to happy
    emotion = session.get('current_emotion', 'happy')
    
    # Select a random affirmation based on emotion
    import random
    daily_affirmation = random.choice(AFFIRMATIONS.get(emotion, AFFIRMATIONS['happy']))
    
    return render_template('affirmation.html', 
                         name=session['user_name'], 
                         affirmation=daily_affirmation,
                         emotion=emotion)

@app.route('/journal')
def journal():
    if 'user_name' not in session:
        flash('Please enter your name first! 😊', 'info')
        return redirect(url_for('home'))
    
    return render_template('journal.html', name=session['user_name'])

@app.route('/save_journal', methods=['POST'])
def save_journal():
    if 'user_name' not in session:
        return redirect(url_for('home'))
    
    journal_entry = request.form.get('journal_entry', '').strip()
    
    if journal_entry:
        # Create filename based on user's name
        username = session['user_name'].lower().replace(' ', '_')
        filename = f"{username}_journal.txt"
        
        # Prepare entry with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry_with_timestamp = f"\n--- {timestamp} ---\n{journal_entry}\n"
        
        try:
            # Ensure the journals directory exists
            os.makedirs('journals', exist_ok=True)
            
            # Save to file in journals directory
            filepath = os.path.join('journals', filename)
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(entry_with_timestamp)
            
            flash('Your journal entry has been saved! Thank you for sharing with me. 📝💕', 'success')
        except Exception as e:
            logging.error(f"Error saving journal entry: {e}")
            flash('Sorry, there was an issue saving your entry. Please try again! 😔', 'error')
    else:
        flash('Please write something before saving your journal entry! ✨', 'info')
    
    return redirect(url_for('journal'))

@app.route('/reset')
def reset_session():
    session.clear()
    flash('Session reset! Feel free to start fresh, bestie! 🌟', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
