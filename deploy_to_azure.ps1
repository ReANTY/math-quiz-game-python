# Math Quiz Game - Azure Deployment Script
# Run this script in PowerShell as Administrator

param(
    [Parameter(Mandatory=$true)]
    [string]$AppName,
    
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroup = "math-quiz-rg",
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "eastus"
)

Write-Host "🚀 Starting Azure Deployment for Math Quiz Game" -ForegroundColor Green
Write-Host "App Name: $AppName" -ForegroundColor Yellow
Write-Host "Resource Group: $ResourceGroup" -ForegroundColor Yellow
Write-Host "Location: $Location" -ForegroundColor Yellow

# Check if Azure CLI is installed
try {
    $azVersion = az version --output tsv
    Write-Host "✅ Azure CLI detected: $azVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI not found. Please install from: https://aka.ms/installazurecliwindows" -ForegroundColor Red
    exit 1
}

# Login to Azure
Write-Host "🔐 Logging in to Azure..." -ForegroundColor Blue
az login

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Azure login failed" -ForegroundColor Red
    exit 1
}

# Create Resource Group
Write-Host "📦 Creating Resource Group: $ResourceGroup" -ForegroundColor Blue
az group create --name $ResourceGroup --location $Location

# Create App Service Plan
Write-Host "🏗️ Creating App Service Plan..." -ForegroundColor Blue
az appservice plan create `
    --name "$AppName-plan" `
    --resource-group $ResourceGroup `
    --sku F1 `
    --is-linux

# Create Web App
Write-Host "🌐 Creating Web App: $AppName" -ForegroundColor Blue
az webapp create `
    --resource-group $ResourceGroup `
    --plan "$AppName-plan" `
    --name $AppName `
    --runtime "PYTHON|3.10"

# Configure startup command
Write-Host "⚙️ Configuring startup command..." -ForegroundColor Blue
az webapp config set `
    --resource-group $ResourceGroup `
    --name $AppName `
    --startup-file "startup.txt"

# Set environment variables
Write-Host "🔧 Setting environment variables..." -ForegroundColor Blue
$secretKey = [System.Web.Security.Membership]::GeneratePassword(32, 8)
az webapp config appsettings set `
    --resource-group $ResourceGroup `
    --name $AppName `
    --settings SECRET_KEY="$secretKey" PYTHONPATH="/home/site/wwwroot"

# Enable HTTPS only
Write-Host "🔒 Enabling HTTPS only..." -ForegroundColor Blue
az webapp update `
    --resource-group $ResourceGroup `
    --name $AppName `
    --https-only true

# Create deployment package
Write-Host "📦 Creating deployment package..." -ForegroundColor Blue
$excludeFiles = @("venv", "__pycache__", "*.pyc", ".git", "*.md", "*.png", "*.pdf", "deploy_to_azure.ps1")
$zipPath = "math-quiz-deployment.zip"

# Use 7-Zip if available, otherwise use built-in compression
if (Get-Command "7z" -ErrorAction SilentlyContinue) {
    7z a $zipPath . -x!venv\ -x!__pycache__\ -x!*.pyc -x!.git\ -x!*.md -x!*.png -x!*.pdf -x!deploy_to_azure.ps1
} else {
    # Fallback to PowerShell compression
    $files = Get-ChildItem -Path . -Recurse | Where-Object { 
        $_.FullName -notmatch "venv|__pycache__|\.pyc$|\.git|\.md$|\.png$|\.pdf$|deploy_to_azure\.ps1" 
    }
    Compress-Archive -Path $files.FullName -DestinationPath $zipPath -Force
}

# Deploy to Azure
Write-Host "🚀 Deploying to Azure..." -ForegroundColor Blue
az webapp deployment source config-zip `
    --resource-group $ResourceGroup `
    --name $AppName `
    --src $zipPath

# Clean up deployment package
Remove-Item $zipPath -ErrorAction SilentlyContinue

# Get the URL
$appUrl = "https://$AppName.azurewebsites.net"

Write-Host ""
Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host "🌐 Your app is available at: $appUrl" -ForegroundColor Cyan
Write-Host "📊 Azure Portal: https://portal.azure.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  Note: It may take a few minutes for the app to start up completely." -ForegroundColor Yellow
Write-Host "🔍 Check logs if needed: az webapp log tail --resource-group $ResourceGroup --name $AppName" -ForegroundColor Yellow

# Ask to open browser
$openBrowser = Read-Host "Open the app in browser? (y/n)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
    Start-Process $appUrl
} 