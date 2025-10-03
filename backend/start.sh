#!/bin/bash
# Script de démarrage pour Render

# Créer les répertoires nécessaires
mkdir -p /opt/render/project/src/data/chroma_db
mkdir -p /opt/render/project/src/data/cache

# Charger les données de démonstration si la base est vide
python scripts/load_demo_data.py || echo "Données déjà chargées ou erreur non bloquante"

# Démarrer l'application
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
