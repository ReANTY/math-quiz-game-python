# Panduan Setup MySQL dengan Laragon untuk Quiz Game

## Prasyarat

1. **Laragon** sudah terinstall dan berjalan
2. **MySQL** service di Laragon sudah aktif
3. **phpMyAdmin** tersedia di Laragon

## Langkah-langkah Setup

### 1. Pastikan Laragon MySQL Berjalan

- Buka Laragon
- Pastikan service **MySQL** sedang running (lampu hijau)
- Jika belum berjalan, klik **Start All** atau **MySQL**

### 2. Install Dependencies Python

```bash
# Aktivasi virtual environment (jika menggunakan)
# venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies baru
pip install -r requirements.txt
```

### 3. Jalankan Script Migrasi

```bash
python migrate_to_mysql.py
```

Script ini akan:

- Membuat database `quiz_game_db` di MySQL
- Membuat tabel yang diperlukan
- Migrasi data dari SQLite (jika ada)

### 4. Verifikasi Database via phpMyAdmin

1. Buka browser dan akses: `http://localhost/phpmyadmin`
2. Login dengan:
   - **Username**: `root`
   - **Password**: (kosong, tekan Enter)
3. Pilih database `quiz_game_db`
4. Periksa tabel yang telah dibuat:
   - `user` - Tabel pengguna
   - `game_result` - Tabel hasil quiz

### 5. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di: `http://localhost:5000`

## Konfigurasi Database

### Default Configuration (Laragon)

```python
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Kosong untuk Laragon default
MYSQL_DATABASE = 'quiz_game_db'
```

### Custom Configuration

Jika Anda ingin menggunakan konfigurasi berbeda, set environment variables:

```bash
# Windows PowerShell
$env:MYSQL_HOST = "localhost"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "yourpassword"
$env:MYSQL_DATABASE = "quiz_game_db"

# Linux/Mac
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=yourpassword
export MYSQL_DATABASE=quiz_game_db
```

## Struktur Database

### Tabel `user`

```sql
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabel `game_result`

```sql
CREATE TABLE game_result (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    score INT NOT NULL,
    total_questions INT DEFAULT 10,
    played_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_taken INT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

## Troubleshooting

### Error: "Access denied for user 'root'"

- Pastikan MySQL service di Laragon berjalan
- Coba reset password MySQL di Laragon
- Periksa konfigurasi user/password

### Error: "Unknown database 'quiz_game_db'"

- Jalankan script migrasi: `python migrate_to_mysql.py`
- Atau buat database manual via phpMyAdmin

### Error: "No module named 'pymysql'"

- Install PyMySQL: `pip install PyMySQL==1.1.0`
- Pastikan virtual environment aktif

### Error koneksi database

- Periksa apakah MySQL port 3306 terbuka
- Restart Laragon
- Periksa firewall/antivirus

## Keuntungan MySQL vs SQLite

### MySQL + phpMyAdmin

✅ Interface visual yang mudah digunakan  
✅ Performa lebih baik untuk data besar  
✅ Mendukung multiple concurrent users  
✅ Backup dan restore yang mudah  
✅ Monitoring dan analisis data yang lebih baik

### SQLite (sebelumnya)

✅ Tidak memerlukan server database  
✅ File database tunggal  
❌ Tidak ada interface visual bawaan  
❌ Terbatas untuk concurrent access

## Backup Database

### Via phpMyAdmin

1. Buka phpMyAdmin
2. Pilih database `quiz_game_db`
3. Klik tab **Export**
4. Pilih format **SQL**
5. Klik **Go** untuk download

### Via Command Line

```bash
mysqldump -u root -p quiz_game_db > backup.sql
```

## Restore Database

```bash
mysql -u root -p quiz_game_db < backup.sql
```

## Akses phpMyAdmin

- **URL**: http://localhost/phpmyadmin
- **Username**: root
- **Password**: (kosong untuk default Laragon)

Selamat! Database MySQL Anda sudah siap digunakan dengan phpMyAdmin! 🎉
