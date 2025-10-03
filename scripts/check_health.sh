#!/bin/bash
# Script pour vérifier la santé du système

set -e

echo "🏥 PharmaBot - Health Check"
echo "============================"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend local
echo -e "\n📡 Backend Local (http://localhost:8000)"
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    HEALTH=$(curl -s http://localhost:8000/api/health | python3 -m json.tool)
    echo -e "${GREEN}✅ Backend LOCAL: OK${NC}"
    echo "$HEALTH"
else
    echo -e "${RED}❌ Backend LOCAL: Inaccessible${NC}"
    echo "   Démarrez le backend avec: cd backend && uvicorn app.main:app --reload"
fi

# Frontend local
echo -e "\n🎨 Frontend Local (http://localhost:5174)"
if curl -s http://localhost:5174 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend LOCAL: OK${NC}"
else
    echo -e "${RED}❌ Frontend LOCAL: Inaccessible${NC}"
    echo "   Démarrez le frontend avec: cd frontend && npm run dev"
fi

# Backend production
echo -e "\n🌍 Backend Production"
PROD_BACKEND="https://pharmabot-backend.onrender.com"
if curl -s "${PROD_BACKEND}/api/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend PROD: OK${NC}"
    curl -s "${PROD_BACKEND}/api/health" | python3 -m json.tool
else
    echo -e "${YELLOW}⚠️  Backend PROD: Peut-être en veille (Render free tier)${NC}"
    echo "   Premier appel peut prendre 30s..."
fi

# Frontend production
echo -e "\n🌐 Frontend Production"
PROD_FRONTEND="https://pharmabot-vidal-assistant.netlify.app"
if curl -s -o /dev/null -w "%{http_code}" "${PROD_FRONTEND}" | grep -q "200"; then
    echo -e "${GREEN}✅ Frontend PROD: OK${NC}"
    echo "   URL: ${PROD_FRONTEND}"
else
    echo -e "${RED}❌ Frontend PROD: Erreur${NC}"
fi

# ChromaDB stats
echo -e "\n📊 Base de données ChromaDB"
if [ -d "backend/data/chroma_db" ]; then
    SIZE=$(du -sh backend/data/chroma_db 2>/dev/null | cut -f1)
    echo -e "${GREEN}✅ ChromaDB présente: ${SIZE}${NC}"
    
    # Essayer d'obtenir les stats
    if command -v python3 &> /dev/null && [ -f "backend/check_db.py" ]; then
        cd backend
        if [ -d "venv" ]; then
            source venv/bin/activate
            python check_db.py 2>/dev/null || echo "   (Stats non disponibles)"
            deactivate
        fi
        cd ..
    fi
else
    echo -e "${YELLOW}⚠️  ChromaDB vide - Exécutez: python backend/scripts/scrape_data.py${NC}"
fi

echo -e "\n✅ Health check terminé"
