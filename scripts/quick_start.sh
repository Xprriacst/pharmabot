#!/bin/bash

# PharmaBot Quick Start Script
# Ce script configure et démarre automatiquement l'application

set -e  # Arrêter en cas d'erreur

echo "🚀 PharmaBot - Quick Start"
echo "=========================="

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé"
    exit 1
fi

echo "✅ Python 3: $(python3 --version)"
echo "✅ Node.js: $(node --version)"
echo ""

# Backend Setup
echo "📦 Configuration du Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

echo "Activation de l'environnement virtuel..."
source venv/bin/activate

echo "Installation des dépendances Python..."
pip install -q -r requirements.txt
python -m spacy download fr_core_news_sm

if [ ! -f ".env" ]; then
    echo "⚠️  Création du fichier .env"
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Configurez votre clé API OpenAI dans backend/.env"
    echo "   OPENAI_API_KEY=sk-votre-clé"
    echo ""
    read -p "Appuyez sur Entrée une fois configuré..."
fi

# Check if data exists
if [ ! -d "data/chroma_db" ]; then
    echo ""
    echo "⚠️  Aucune donnée trouvée. Lancement du scraping..."
    echo "   Cela peut prendre 10-30 minutes"
    read -p "Continuer? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python scripts/scrape_data.py
    else
        echo "⚠️  Vous devrez lancer manuellement: python scripts/scrape_data.py"
    fi
fi

cd ..

# Frontend Setup
echo ""
echo "📦 Configuration du Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installation des dépendances Node.js..."
    npm install
fi

if [ ! -f ".env" ]; then
    cp .env.example .env
fi

cd ..

echo ""
echo "✅ Configuration terminée!"
echo ""
echo "Pour démarrer l'application:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Puis ouvrir: http://localhost:5173"
