import random
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import pymysql
from config import config

# Install PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# Load configuration based on environment
config_name = os.environ.get('FLASK_ENV', 'development')
if os.environ.get('WEBSITE_SITE_NAME'):  # Azure environment
    config_name = 'production'

app.config.from_object(config[config_name])

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    game_results = db.relationship('GameResult', backref='player', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class GameResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, default=10)
    played_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_taken = db.Column(db.Integer, nullable=True)  # in seconds

    def __repr__(self):
        return f'<GameResult {self.score}/{self.total_questions}>'

# Create tables
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")

def generate_question():
    """
    Menghasilkan soal matematika acak dan jawabannya.
    Operasi yang digunakan: +, -, *, /
    Untuk operasi pembagian, soal disusun agar hasil berupa bilangan bulat.
    """
    ops = ['+', '-', '*', '/']
    op = random.choice(ops)
    
    if op == '+':
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        question = f"{a} + {b}"
        answer = a + b
    elif op == '-':
        a = random.randint(0, 100)
        b = random.randint(0, a)  # pastikan tidak negatif
        question = f"{a} - {b}"
        answer = a - b
    elif op == '*':
        a = random.randint(0, 12)
        b = random.randint(0, 12)
        question = f"{a} * {b}"
        answer = a * b
    elif op == '/':
        b = random.randint(1, 12)
        answer = random.randint(1, 12)
        a = b * answer
        question = f"{a} / {b}"
        # Jawaban adalah bilangan bulat
    return question, answer

@app.route('/')
def home():
    # Halaman landing atau start quiz
    return render_template('start.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        
        if not username or not email:
            flash('Username dan email harus diisi!', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email sudah digunakan!', 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        flash(f'Selamat datang {username}!', 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        
        if not username:
            flash('Username harus diisi!', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Selamat datang kembali {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Username tidak ditemukan!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('home'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu untuk bermain!', 'warning')
        return redirect(url_for('login'))
    
    # Inisialisasi sesi game jika belum ada
    if 'round' not in session:
        session['round'] = 1
        session['score'] = 0
        session['start_time'] = datetime.now().timestamp()
        question, answer = generate_question()
        session['question'] = question
        session['correct_answer'] = answer

    # Saat menerima input jawaban
    if request.method == 'POST':
        user_answer = request.form.get('answer', '').strip()
        try:
            # Gunakan float untuk cek jawaban (soal pembagian menghasilkan bilangan bulat)
            user_answer = float(user_answer)
        except:
            # Jika input tidak valid, asumsikan jawaban salah
            user_answer = None
        
        correct_answer = session.get('correct_answer')
        if user_answer == correct_answer:
            session['score'] += 1
            feedback = "Benar!"
        else:
            feedback = f"Salah! Jawaban yang benar adalah {correct_answer}."
        session['last_feedback'] = feedback

        # Lanjutkan ke ronde berikutnya atau akhiri game setelah 10 ronde
        round_number = session['round']
        if round_number < 10:
            session['round'] = round_number + 1
            question, answer = generate_question()
            session['question'] = question
            session['correct_answer'] = answer
            return redirect(url_for('quiz'))
        else:
            # Save game result to database
            end_time = datetime.now().timestamp()
            time_taken = int(end_time - session.get('start_time', end_time))
            
            game_result = GameResult(
                user_id=session['user_id'],
                score=session['score'],
                total_questions=10,
                time_taken=time_taken
            )
            db.session.add(game_result)
            db.session.commit()
            
            return redirect(url_for('result'))
        
    return render_template('quiz.html',
                           question=session.get('question'),
                           round=session.get('round'),
                           score=session.get('score'),
                           last_feedback=session.pop('last_feedback', None),
                           username=session.get('username'))

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = 10
    username = session.get('username', 'Guest')
    
    # Get user's best score
    if 'user_id' in session:
        best_result = GameResult.query.filter_by(user_id=session['user_id']).order_by(GameResult.score.desc()).first()
        best_score = best_result.score if best_result else 0
    else:
        best_score = 0
    
    # Kosongkan sesi game setelah selesai permainan (tapi tetap login)
    game_keys = ['round', 'score', 'question', 'correct_answer', 'last_feedback', 'start_time']
    for key in game_keys:
        session.pop(key, None)
    
    return render_template('result.html', 
                         score=score, 
                         total=total, 
                         username=username,
                         best_score=best_score)

@app.route('/leaderboard')
def leaderboard():
    # Get top 10 best scores
    top_scores = db.session.query(
        User.username,
        db.func.max(GameResult.score).label('best_score'),
        db.func.count(GameResult.id).label('games_played'),
        db.func.avg(GameResult.score).label('avg_score')
    ).join(GameResult).group_by(User.id).order_by(db.func.max(GameResult.score).desc()).limit(10).all()
    
    # Get recent games
    recent_games = db.session.query(
        User.username,
        GameResult.score,
        GameResult.played_at
    ).join(GameResult).order_by(GameResult.played_at.desc()).limit(5).all()
    
    return render_template('leaderboard.html', 
                         top_scores=top_scores, 
                         recent_games=recent_games)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu!', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    game_results = GameResult.query.filter_by(user_id=session['user_id']).order_by(GameResult.played_at.desc()).all()
    
    # Calculate statistics
    if game_results:
        best_score = max(result.score for result in game_results)
        avg_score = sum(result.score for result in game_results) / len(game_results)
        total_games = len(game_results)
    else:
        best_score = avg_score = total_games = 0
    
    return render_template('profile.html', 
                         user=user, 
                         game_results=game_results,
                         best_score=best_score,
                         avg_score=round(avg_score, 1),
                         total_games=total_games)

@app.route('/reset')
def reset():
    # Only clear game session, keep login session
    game_keys = ['round', 'score', 'question', 'correct_answer', 'last_feedback', 'start_time']
    for key in game_keys:
        session.pop(key, None)
    return redirect(url_for('home'))

# Health check endpoint for Azure
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'app': 'Math Quiz Game'}, 200

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
