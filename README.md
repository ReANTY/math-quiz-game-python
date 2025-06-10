# 🧮 Math Quiz Game dengan Database

Aplikasi web quiz matematika interaktif yang dibuat dengan Flask dan SQLAlchemy. Aplikasi ini memungkinkan pengguna untuk bermain quiz matematika, menyimpan skor, dan melihat leaderboard.

## ✨ Fitur Utama

### 🎮 Gameplay

- Quiz matematika dengan 10 pertanyaan acak
- Operasi: penjumlahan (+), pengurangan (-), perkalian (×), pembagian (÷)
- Timer 10 detik per soal
- Feedback real-time untuk setiap jawaban

### 👤 Sistem User

- **Registrasi & Login**: Sistem autentikasi sederhana
- **Profil Pengguna**: Statistik personal dan riwayat game
- **Session Management**: Login persistent dengan keamanan session

### 📊 Database & Statistik

- **Riwayat Skor**: Semua hasil quiz tersimpan otomatis
- **Leaderboard**: Ranking 10 pemain terbaik
- **Statistik Personal**:
  - Skor terbaik
  - Rata-rata skor
  - Total game dimainkan
  - Waktu penyelesaian per game

### 🏆 Fitur Kompetitif

- **Top Scorers**: Medal sistem (🥇🥈🥉) untuk 3 teratas
- **Recent Games**: Aktivitas game terbaru dari semua pemain
- **Achievement**: Notifikasi untuk skor terbaik baru

## 🚀 Cara Menjalankan

### 1. Persiapan Environment

```bash
# Aktifkan virtual environment (jika ada)
venv\Scripts\activate  # Windows
# atau
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi

```bash
python app.py
```

### 3. Buka Browser

Akses aplikasi di: `http://localhost:5000`

## 🗄️ Struktur Database

### Tabel `User`

```sql
- id (Primary Key)
- username (Unique)
- email (Unique)
- created_at (Timestamp)
```

### Tabel `GameResult`

```sql
- id (Primary Key)
- user_id (Foreign Key → User.id)
- score (Integer 0-10)
- total_questions (Default: 10)
- played_at (Timestamp)
- time_taken (Seconds)
```

## 📁 Struktur Folder

```
math-quiz-game/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── quiz_game.db          # SQLite database (auto-generated)
├── static/
│   └── style.css         # CSS styling
├── templates/
│   ├── start.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── quiz.html         # Quiz gameplay
│   ├── result.html       # Game results
│   ├── leaderboard.html  # Leaderboard & recent games
│   └── profile.html      # User profile & history
└── venv/                 # Virtual environment
```

## 🎯 Cara Bermain

1. **Daftar/Login**: Buat akun baru atau login dengan username yang sudah ada
2. **Mulai Quiz**: Klik "Start Quiz" di homepage
3. **Jawab Soal**: Masukkan jawaban dalam 10 detik per soal
4. **Lihat Hasil**: Skor dan statistik akan ditampilkan di akhir
5. **Cek Leaderboard**: Lihat ranking dan bandingkan dengan pemain lain

## 🛠️ Teknologi yang Digunakan

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy + SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS dengan responsive design
- **Session**: Flask session management

## 🎨 Fitur UI/UX

- **Responsive Design**: Berfungsi di desktop dan mobile
- **Modern Interface**: Gradient background dan card-based layout
- **Flash Messages**: Notifikasi sukses, error, dan warning
- **Smooth Animations**: Hover effects dan transitions
- **Color-coded Elements**:
  - Hijau untuk sukses/skor tinggi
  - Merah untuk error/timer
  - Biru untuk navigation
  - Medal colors untuk top 3 leaderboard

## 📈 Pengembangan Selanjutnya

Fitur yang bisa ditambahkan:

- [ ] Sistem password yang aman (hashing)
- [ ] Level kesulitan (Easy, Medium, Hard)
- [ ] Kategori soal yang lebih beragam
- [ ] Challenge antar teman
- [ ] Export statistik ke PDF
- [ ] Push notifications untuk achievement
- [ ] Dark mode theme
- [ ] Multiplayer real-time

## 🐛 Troubleshooting

### Database tidak terbuat otomatis

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Error saat install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Port sudah digunakan

Ubah port di `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Ganti port
```

## 👥 Kontribusi

Silakan fork repository ini dan submit pull request untuk improvement atau bug fixes.

## 📄 Lisensi

Project ini dibuat untuk tujuan edukasi dan pembelajaran Flask web development.

---

**Happy Quizzing! 🎉**
