#!/bin/bash
# Script pour exécuter les tests backend avec différentes options

set -e

echo "🧪 PharmaBot - Tests Backend"
echo "=============================="

# Activer l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Exécutez 'python -m venv venv' d'abord."
    exit 1
fi

source venv/bin/activate

# Vérifier que pytest est installé
if ! command -v pytest &> /dev/null; then
    echo "📦 Installation de pytest..."
    pip install pytest pytest-asyncio pytest-cov
fi

# Mode par défaut: tous les tests avec couverture
MODE=${1:-all}

case $MODE in
    fast)
        echo "⚡ Mode rapide - Tests uniquement"
        pytest tests/ -v
        ;;
    coverage)
        echo "📊 Mode coverage - Tests avec rapport détaillé"
        pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html
        echo ""
        echo "📄 Rapport HTML généré dans: htmlcov/index.html"
        ;;
    watch)
        echo "👀 Mode watch - Relance automatique"
        pytest-watch tests/
        ;;
    *)
        echo "🔍 Mode complet - Tests avec couverture"
        pytest tests/ -v --cov=app --cov-report=term-missing
        ;;
esac

echo ""
echo "✅ Tests terminés"
