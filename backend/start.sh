#!/bin/bash
# Script de démarrage pour Render

# Créer les répertoires nécessaires
mkdir -p data/chroma_db
mkdir -p data/cache

# Démarrer l'application immédiatement
echo "🚀 Démarrage de l'application..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
