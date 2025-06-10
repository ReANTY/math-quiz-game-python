# 🚀 Quick Deploy Azure dengan MySQL Support

## 📋 **Ringkasan Perubahan untuk MySQL**

Setelah migrasi ke MySQL, ada **2 opsi deployment** ke Azure:

### ✅ **Opsi 1: Deploy dengan SQLite (Termudah & Gratis)**

- **Database**: Auto-fallback ke SQLite
- **Cost**: 100% Free
- **Setup Time**: 5 menit
- **Recommended for**: Testing, demo, personal use

### ✅ **Opsi 2: Deploy dengan Azure MySQL (Production)**

- **Database**: Azure Database for MySQL
- **Cost**: ~$15-50/month
- **Setup Time**: 15 menit
- **Recommended for**: Production, persistent data

## 🚀 **Quick Deploy - SQLite (Recommended)**

### **Step 1: Login & Setup**

```powershell
# Login ke Azure
az login

# Create resource group
az group create --name math-quiz-rg --location eastus
```

### **Step 2: Create App Service**

```powershell
# Create app service plan
az appservice plan create --name math-quiz-plan --resource-group math-quiz-rg --sku F1 --is-linux

# Create web app
az webapp create --resource-group math-quiz-rg --plan math-quiz-plan --name math-quiz-game-YOURNAME --runtime "PYTHON|3.10"
```

### **Step 3: Configure Environment**

```powershell
# Set environment variables
az webapp config appsettings set --resource-group math-quiz-rg --name math-quiz-game-YOURNAME --settings SECRET_KEY="your-secret-key" FLASK_ENV="production"

# Set startup command
az webapp config set --resource-group math-quiz-rg --name math-quiz-game-YOURNAME --startup-file "startup.txt"
```

### **Step 4: Deploy Code**

- **Option A**: Via Azure Portal → Deployment Center → GitHub
- **Option B**: Via VS Code Azure Extension
- **Option C**: Manual ZIP upload

## 🗄️ **Upgrade ke MySQL (Optional)**

### **Create Azure MySQL**

```powershell
# Create MySQL Flexible Server
az mysql flexible-server create \
    --resource-group math-quiz-rg \
    --name math-quiz-mysql \
    --location eastus \
    --admin-user mysqladmin \
    --admin-password "YourPassword123!" \
    --sku-name Standard_B1ms \
    --tier Burstable

# Create database
az mysql flexible-server db create \
    --resource-group math-quiz-rg \
    --server-name math-quiz-mysql \
    --database-name quiz_game_db

# Configure firewall
az mysql flexible-server firewall-rule create \
    --resource-group math-quiz-rg \
    --name math-quiz-mysql \
    --rule-name AllowAzure \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0
```

### **Update App Settings**

```powershell
az webapp config appsettings set \
    --resource-group math-quiz-rg \
    --name math-quiz-game-YOURNAME \
    --settings \
        AZURE_MYSQL_HOST="math-quiz-mysql.mysql.database.azure.com" \
        AZURE_MYSQL_USER="mysqladmin" \
        AZURE_MYSQL_PASSWORD="YourPassword123!" \
        AZURE_MYSQL_DATABASE="quiz_game_db"
```

## ⚡ **Apa yang Berubah dari Sebelumnya?**

### 🔄 **Konfigurasi Database (config.py)**

- ✅ **Auto-detection**: Deteksi otomatis Azure MySQL vs SQLite
- ✅ **Fallback**: Jika MySQL tidak tersedia, otomatis pakai SQLite
- ✅ **Environment variables**: Support Azure MySQL environment variables

### 📁 **File Structure**

- ✅ **Lebih bersih**: File tidak perlu sudah dihapus
- ✅ **MySQL support**: PyMySQL sudah ditambahkan ke requirements.txt
- ✅ **Documentation**: Panduan lengkap MySQL setup

### 🚀 **Deployment Process**

- ✅ **Sama seperti sebelumnya**: Proses deployment tidak berubah
- ✅ **Database otomatis**: Tabel dibuat otomatis saat pertama akses
- ✅ **Zero downtime**: Fallback ke SQLite jika MySQL tidak tersedia

## 💡 **Rekomendasi**

### 🎯 **Untuk Development/Testing**

```bash
Deploy dengan SQLite (gratis) → Test aplikasi → Upgrade ke MySQL jika diperlukan
```

### 🎯 **Untuk Production**

```bash
Deploy langsung dengan Azure MySQL → Backup otomatis → Scaling mudah
```

## 🔧 **Migration dari Local MySQL**

### **Export dari Local (Laragon)**

1. Buka phpMyAdmin: `http://localhost:8000/phpmyadmin`
2. Pilih database `quiz_game_db`
3. Export → SQL format → Download

### **Import ke Azure MySQL**

1. Install MySQL Workbench
2. Connect ke Azure MySQL server
3. Import SQL file yang sudah diexport

## ✅ **Ready to Deploy!**

**Project Anda sudah siap deploy dengan konfigurasi baru:**

- ✅ Database flexible (MySQL/SQLite)
- ✅ File structure bersih
- ✅ Documentation lengkap
- ✅ Zero breaking changes

**Pilih opsi deployment yang sesuai budget dan kebutuhan Anda!** 🎉
