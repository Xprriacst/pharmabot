#!/bin/bash
# Script de démarrage pour Render

# Créer les répertoires nécessaires
mkdir -p data/chroma_db
mkdir -p data/cache

# Charger les données de démonstration
echo "🔄 Chargement des données de démonstration..."
python scripts/load_demo_data.py

# Démarrer l'application
echo "🚀 Démarrage de l'application..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
