#!/bin/bash

# Math Quiz Game - Azure Deployment Script
# Usage: ./deploy_to_azure.sh <app-name> [resource-group] [location]

set -e

# Default values
APP_NAME=""
RESOURCE_GROUP="math-quiz-rg"
LOCATION="eastus"

# Parse arguments
if [ $# -eq 0 ]; then
    echo "❌ Error: App name is required"
    echo "Usage: ./deploy_to_azure.sh <app-name> [resource-group] [location]"
    echo "Example: ./deploy_to_azure.sh my-math-quiz"
    exit 1
fi

APP_NAME=$1
if [ $# -ge 2 ]; then
    RESOURCE_GROUP=$2
fi
if [ $# -ge 3 ]; then
    LOCATION=$3
fi

echo "🚀 Starting Azure Deployment for Math Quiz Game"
echo "App Name: $APP_NAME"
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Please install it first:"
    echo "   Mac: brew install azure-cli"
    echo "   Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
    exit 1
fi

echo "✅ Azure CLI detected: $(az version --query '"azure-cli"' -o tsv)"

# Login to Azure
echo "🔐 Logging in to Azure..."
az login

# Create Resource Group
echo "📦 Creating Resource Group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan
echo "🏗️ Creating App Service Plan..."
az appservice plan create \
    --name "${APP_NAME}-plan" \
    --resource-group $RESOURCE_GROUP \
    --sku F1 \
    --is-linux

# Create Web App
echo "🌐 Creating Web App: $APP_NAME"
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan "${APP_NAME}-plan" \
    --name $APP_NAME \
    --runtime "PYTHON|3.10"

# Configure startup command
echo "⚙️ Configuring startup command..."
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --startup-file "startup.txt"

# Generate secret key
SECRET_KEY=$(openssl rand -hex 32)

# Set environment variables
echo "🔧 Setting environment variables..."
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --settings SECRET_KEY="$SECRET_KEY" PYTHONPATH="/home/site/wwwroot"

# Enable HTTPS only
echo "🔒 Enabling HTTPS only..."
az webapp update \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --https-only true

# Create deployment package
echo "📦 Creating deployment package..."
ZIP_FILE="math-quiz-deployment.zip"

# Remove old zip if exists
rm -f $ZIP_FILE

# Create zip excluding unnecessary files
zip -r $ZIP_FILE . \
    -x "venv/*" \
       "__pycache__/*" \
       "*.pyc" \
       ".git/*" \
       "*.md" \
       "*.png" \
       "*.pdf" \
       "deploy_to_azure.sh" \
       "deploy_to_azure.ps1"

# Deploy to Azure
echo "🚀 Deploying to Azure..."
az webapp deployment source config-zip \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --src $ZIP_FILE

# Clean up deployment package
rm -f $ZIP_FILE

# Get the URL
APP_URL="https://${APP_NAME}.azurewebsites.net"

echo ""
echo "🎉 Deployment completed successfully!"
echo "🌐 Your app is available at: $APP_URL"
echo "📊 Azure Portal: https://portal.azure.com"
echo ""
echo "⚠️  Note: It may take a few minutes for the app to start up completely."
echo "🔍 Check logs if needed: az webapp log tail --resource-group $RESOURCE_GROUP --name $APP_NAME"

# Ask to open browser (Linux with GUI)
if command -v xdg-open &> /dev/null; then
    read -p "Open the app in browser? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open $APP_URL
    fi
# Mac
elif command -v open &> /dev/null; then
    read -p "Open the app in browser? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open $APP_URL
    fi
fi

echo "✅ Done!" 