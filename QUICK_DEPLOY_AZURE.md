# ⚡ Quick Deploy ke Azure - Math Quiz Game

## 🎯 **3 Cara Tercepat Deploy ke Azure**

### **🚀 Cara 1: Automated Script (Termudah)**

#### **Windows (PowerShell):**

```powershell
# Buka PowerShell as Administrator
# Ganti "my-math-quiz" dengan nama unik Anda
.\deploy_to_azure.ps1 -AppName "my-math-quiz"
```

#### **Linux/Mac (Bash):**

```bash
# Buat script executable
chmod +x deploy_to_azure.sh

# Deploy (ganti nama dengan unik)
./deploy_to_azure.sh my-math-quiz
```

### **🌐 Cara 2: Azure Portal (No Code)**

1. **Login** → [portal.azure.com](https://portal.azure.com)
2. **Create Resource** → **App Service**
3. **Settings:**
   - Name: `math-quiz-yourname` (harus unik)
   - Runtime: `Python 3.10`
   - OS: `Linux`
   - Plan: `F1 (Free)`
4. **Create** → **Go to resource**
5. **Deployment Center** → **Local Git** atau **GitHub**
6. **Upload files** via **App Service Editor**

### **💻 Cara 3: VS Code Extension**

1. **Install Extension:** `Azure App Service`
2. **Login** ke Azure account
3. **Right-click** project folder → **Deploy to Web App**
4. **Select** atau **Create new** App Service
5. **Done!**

---

## 📋 **Prerequisites (Install Dulu)**

### **Azure CLI** (untuk Script)

- **Windows:** [Download Installer](https://aka.ms/installazurecliwindows)
- **Mac:** `brew install azure-cli`
- **Linux:** `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`

### **Azure Account**

- **Free Account:** [azure.microsoft.com/free](https://azure.microsoft.com/free)
- **Student:** [azure.microsoft.com/student](https://azure.microsoft.com/student) (Credit $100)

---

## ⚡ **Fastest Path (5 Menit)**

```bash
# 1. Download Azure CLI
# 2. Open terminal di project folder
# 3. Run script:

# Windows:
.\deploy_to_azure.ps1 -AppName "quiz-[yourname]"

# Mac/Linux:
./deploy_to_azure.sh quiz-yourname

# 4. Login to Azure when prompted
# 5. Wait for deployment (2-3 minutes)
# 6. Open URL: https://quiz-yourname.azurewebsites.net
```

---

## 🎊 **Hasil Akhir**

Setelah deployment berhasil:

✅ **URL Live:** `https://your-app-name.azurewebsites.net`  
✅ **HTTPS Enabled:** Automatic SSL certificate  
✅ **Database Working:** SQLite persistent storage  
✅ **All Features:** Registration, Login, Quiz, Leaderboard

---

## 🔧 **Troubleshooting Cepat**

### **Error: App name already exists**

```bash
# Ganti nama app dengan unik
./deploy_to_azure.sh quiz-yourname-$(date +%s)
```

### **Error: Azure CLI not found**

```bash
# Install Azure CLI terlebih dahulu
# Windows: https://aka.ms/installazurecliwindows
# Mac: brew install azure-cli
```

### **App tidak load**

```bash
# Check logs
az webapp log tail --resource-group math-quiz-rg --name your-app-name

# Restart app
az webapp restart --resource-group math-quiz-rg --name your-app-name
```

---

## 💰 **Biaya**

- **Free Tier (F1):** $0/month

  - ✅ 1GB storage, 1 hour CPU/day
  - ❌ Custom domain, always-on

- **Basic (B1):** ~$13/month
  - ✅ Custom domain, always-on
  - ✅ 1.75GB RAM, better performance

---

## 🎯 **Next Steps Setelah Deploy**

1. **Test semua fitur** - register, login, main quiz
2. **Share URL** dengan teman untuk testing
3. **Custom domain** (jika diperlukan)
4. **Monitor usage** di Azure Portal
5. **Backup database** secara berkala

---

**Happy Deploying! 🚀**

_Aplikasi Math Quiz Game Anda sekarang live di cloud!_
