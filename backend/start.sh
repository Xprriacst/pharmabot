#!/bin/bash
# Script de démarrage pour Render

# Créer les répertoires nécessaires
mkdir -p data/chroma_db
mkdir -p data/cache

# Charger les données de démonstration en arrière-plan
echo "🔄 Chargement des données de démonstration en arrière-plan..."
nohup python scripts/load_demo_data.py > /dev/null 2>&1 &

# Démarrer l'application immédiatement
echo "🚀 Démarrage de l'application..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
