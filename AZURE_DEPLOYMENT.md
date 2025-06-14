# 🌐 Panduan Deploy Math Quiz Game ke Azure

Panduan lengkap untuk deploy aplikasi Math Quiz Game ke **Azure App Service** dengan opsi **MySQL Database**.

## 📋 **Prerequisites**

### 1. **Akun Azure**

- Daftar di [portal.azure.com](https://portal.azure.com)
- Bisa menggunakan **Free Tier** untuk testing

### 2. **Tools yang Dibutuhkan**

```bash
# Install Azure CLI
# Windows: Download dari https://aka.ms/installazurecliwindows
# Mac: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install Git (jika belum ada)
# Download dari https://git-scm.com/download
```

## 🗄️ **Opsi Database untuk Azure**

### **Opsi 1: SQLite (Default/Fallback)**

- ✅ **Pros**: Simple, no additional cost, auto-fallback
- ❌ **Cons**: Data akan hilang saat redeploy, tidak persistent
- 💰 **Cost**: Free

### **Opsi 2: Azure Database for MySQL (Recommended)**

- ✅ **Pros**: Persistent data, scalable, managed service, backup otomatis
- ✅ **Perfect for**: Production apps, data persistence
- 💰 **Cost**: ~$15-50/month (tergantung tier)

### **Opsi 3: Azure SQL Database**

- ✅ **Pros**: Enterprise grade, advanced features
- ❌ **Cons**: Lebih mahal, perlu modify code
- 💰 **Cost**: ~$25-100/month

## 🚀 **Deploy dengan SQLite (Termudah)**

### **Step 1: Quick Deploy**

## 🚀 **Metode 1: Deploy via Azure Portal (Termudah)**

### **Step 1: Siapkan Repository**

```bash
# Di folder project Anda
git init
git add .
git commit -m "Initial commit - Math Quiz Game"

# Push ke GitHub/GitLab (opsional tapi recommended)
```

### **Step 2: Buat Azure App Service**

1. **Login ke Azure Portal** → [portal.azure.com](https://portal.azure.com)

2. **Create Resource** → **App Service**

3. **Konfigurasi:**

   ```
   Resource Group: math-quiz-rg (create new)
   Name: math-quiz-game-[yourname]
   Runtime Stack: Python 3.10
   Operating System: Linux
   Region: East US (atau terdekat)
   Pricing Plan: F1 (Free) untuk testing
   ```

4. **Click "Review + Create"** → **Create**

### **Step 3: Deploy Code**

**Option A: Drag & Drop (Termudah)**

1. Masuk ke App Service yang sudah dibuat
2. **Development Tools** → **App Service Editor**
3. Drag & drop semua file project ke editor

**Option B: VS Code Extension**

1. Install **Azure App Service** extension di VS Code
2. Login ke Azure account
3. Right-click App Service → **Deploy to Web App**

**Option C: GitHub Actions**

1. Push code ke GitHub repository
2. Di Azure Portal → **Deployment Center**
3. Connect ke GitHub repo
4. Azure akan auto-deploy setiap kali ada push

## 🚀 **Metode 2: Deploy via Azure CLI**

### **Step 1: Setup Azure CLI**

```bash
# Login ke Azure
az login

# Set subscription (jika punya multiple)
az account set --subscription "Your Subscription Name"

# Create resource group
az group create --name math-quiz-rg --location eastus
```

### **Step 2: Create App Service Plan**

```bash
# Create App Service Plan (Free tier)
az appservice plan create \
    --name math-quiz-plan \
    --resource-group math-quiz-rg \
    --sku F1 \
    --is-linux
```

### **Step 3: Create Web App**

```bash
# Create Web App
az webapp create \
    --resource-group math-quiz-rg \
    --plan math-quiz-plan \
    --name math-quiz-game-yourname \
    --runtime "PYTHON|3.10"
```

### **Step 4: Configure Startup Command**

```bash
# Set startup command
az webapp config set \
    --resource-group math-quiz-rg \
    --name math-quiz-game-yourname \
    --startup-file startup.txt
```

### **Step 5: Deploy Code**

```bash
# Deploy via ZIP
zip -r math-quiz.zip . -x "venv/*" "__pycache__/*" "*.pyc"

az webapp deployment source config-zip \
    --resource-group math-quiz-rg \
    --name math-quiz-game-yourname \
    --src math-quiz.zip
```

## ⚙️ **Konfigurasi Environment Variables**

### **Via Azure Portal:**

1. App Service → **Configuration** → **Application Settings**
2. Tambahkan:
   ```
   SECRET_KEY = your-super-secret-key-here
   PYTHONPATH = /home/site/wwwroot
   ```

### **Via Azure CLI:**

```bash
az webapp config appsettings set \
    --resource-group math-quiz-rg \
    --name math-quiz-game-yourname \
    --settings SECRET_KEY="your-super-secret-key-here"
```

## 🚀 **Deploy dengan Azure Database for MySQL (Production)**

### **Step 1: Create Azure Database for MySQL**

```bash
# Create Azure Database for MySQL (Flexible Server)
az mysql flexible-server create \
    --resource-group math-quiz-rg \
    --name math-quiz-mysql-server \
    --location eastus \
    --admin-user mysqladmin \
    --admin-password YourStrongPassword123! \
    --sku-name Standard_B1ms \
    --tier Burstable \
    --storage-size 20 \
    --version 8.0.21

# Create database
az mysql flexible-server db create \
    --resource-group math-quiz-rg \
    --server-name math-quiz-mysql-server \
    --database-name quiz_game_db
```

### **Step 2: Configure Firewall**

```bash
# Allow Azure services
az mysql flexible-server firewall-rule create \
    --resource-group math-quiz-rg \
    --name math-quiz-mysql-server \
    --rule-name AllowAzureServices \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0

# Allow your IP (for management)
az mysql flexible-server firewall-rule create \
    --resource-group math-quiz-rg \
    --name math-quiz-mysql-server \
    --rule-name AllowMyIP \
    --start-ip-address YOUR_IP \
    --end-ip-address YOUR_IP
```

### **Step 3: Set Environment Variables**

```bash
# Set MySQL environment variables for App Service
az webapp config appsettings set \
    --resource-group math-quiz-rg \
    --name math-quiz-game-yourname \
    --settings \
        AZURE_MYSQL_HOST="math-quiz-mysql-server.mysql.database.azure.com" \
        AZURE_MYSQL_USER="mysqladmin" \
        AZURE_MYSQL_PASSWORD="YourStrongPassword123!" \
        AZURE_MYSQL_DATABASE="quiz_game_db" \
        SECRET_KEY="your-super-secret-key-here"
```

### **Step 4: Initialize Database**

Setelah deploy, database akan otomatis membuat tabel saat pertama kali diakses.

## 🗄️ **Database Migration Guide**

### **Dari Local MySQL ke Azure MySQL**

1. **Export data dari local:**

```bash
# Di Laragon/local MySQL
mysqldump -u root -p quiz_game_db > backup.sql
```

2. **Import ke Azure MySQL:**

```bash
# Connect ke Azure MySQL
mysql -h math-quiz-mysql-server.mysql.database.azure.com \
      -u mysqladmin \
      -p quiz_game_db < backup.sql
```

### **Via phpMyAdmin (Easier)**

1. **Export** dari local phpMyAdmin:
   - Pilih database `quiz_game_db`
   - Export → SQL format
2. **Import** ke Azure MySQL:
   - Gunakan MySQL Workbench atau
   - Azure Database for MySQL portal

## 🗄️ **Database Considerations Legacy**

### **SQLite (Fallback)**

- ✅ **Pros**: Simple, no additional cost, auto-fallback
- ❌ **Cons**: Data akan hilang saat redeploy, tidak persistent

### **Azure SQL Database** (Alternative)

```bash
# Create Azure SQL Database
az sql server create \
    --name math-quiz-sql-server \
    --resource-group math-quiz-rg \
    --location eastus \
    --admin-user sqladmin \
    --admin-password YourStrongPassword123!

az sql db create \
    --resource-group math-quiz-rg \
    --server math-quiz-sql-server \
    --name math-quiz-db \
    --service-objective S0
```

## 🔧 **Troubleshooting**

### **1. App Not Starting**

```bash
# Check logs
az webapp log tail --resource-group math-quiz-rg --name math-quiz-game-yourname

# Enable logging
az webapp log config --resource-group math-quiz-rg --name math-quiz-game-yourname --application-logging filesystem
```

### **2. Database Issues**

```bash
# SSH into app
az webapp ssh --resource-group math-quiz-rg --name math-quiz-game-yourname

# Check if database file exists
ls -la /home/site/wwwroot/
```

### **3. Import Errors**

- Pastikan `requirements.txt` lengkap
- Check Python version compatibility

## 🔒 **Security Best Practices**

### **1. Environment Variables**

```bash
# Set production secret key
az webapp config appsettings set \
    --resource-group math-quiz-rg \
    --name math-quiz-game-yourname \
    --settings SECRET_KEY="$(openssl rand -hex 32)"
```

### **2. HTTPS Only**

```bash
# Force HTTPS
az webapp update \
    --resource-group math-quiz-rg \
    --name math-quiz-game-yourname \
    --https-only true
```

### **3. Custom Domain (Optional)**

```bash
# Add custom domain
az webapp config hostname add \
    --resource-group math-quiz-rg \
    --webapp-name math-quiz-game-yourname \
    --hostname yourdomain.com
```

## 💰 **Cost Optimization**

### **Free Tier Limitations:**

- ✅ **Included**: 1GB storage, 1 hour CPU time/day
- ❌ **Limited**: Custom domains, auto-scaling
- ❌ **No**: Always-on, backup

### **Upgrade Options:**

```
Basic B1: $13/month - Custom domains, 1.75GB RAM
Standard S1: $56/month - Auto-scaling, backup
Premium P1V2: $73/month - Better performance
```

## 📊 **Monitoring & Logs**

### **Application Insights**

```bash
# Enable Application Insights
az monitor app-insights component create \
    --app math-quiz-insights \
    --location eastus \
    --resource-group math-quiz-rg
```

### **View Logs**

```bash
# Real-time logs
az webapp log tail --resource-group math-quiz-rg --name math-quiz-game-yourname

# Download logs
az webapp log download --resource-group math-quiz-rg --name math-quiz-game-yourname
```

## 🎯 **Post-Deployment Checklist**

- [ ] ✅ App loads successfully
- [ ] ✅ Registration works
- [ ] ✅ Login works
- [ ] ✅ Quiz gameplay functional
- [ ] ✅ Database saves scores
- [ ] ✅ Leaderboard displays
- [ ] ✅ HTTPS enabled
- [ ] ✅ Custom domain (if needed)
- [ ] ✅ Monitoring setup

## 🔄 **Continuous Deployment**

### **GitHub Actions** (Recommended)

File: `.github/workflows/main.yml`

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Deploy to Azure
        uses: azure/webapps-deploy@v2
        with:
          app-name: "math-quiz-game-yourname"
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

## 📞 **Support & Resources**

- **Azure Documentation**: [docs.microsoft.com/azure](https://docs.microsoft.com/azure)
- **Python on Azure**: [docs.microsoft.com/azure/app-service/quickstart-python](https://docs.microsoft.com/azure/app-service/quickstart-python)
- **Azure Free Account**: [azure.microsoft.com/free](https://azure.microsoft.com/free)

---

## 🎊 **Hasil Akhir**

Setelah deployment berhasil, aplikasi Anda akan accessible di:

```
https://math-quiz-game-yourname.azurewebsites.net
```

**Fitur yang berfungsi:**

- ✅ Math Quiz Game dengan database
- ✅ User registration & login
- ✅ Leaderboard & scoring
- ✅ Responsive design
- ✅ Persistent data storage
- ✅ Professional URL

**Selamat! Aplikasi Anda sudah live di cloud! 🚀**

# Double-click file atau jalankan:

setup_mysql.bat
