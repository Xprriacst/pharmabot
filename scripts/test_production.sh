#!/bin/bash
# Test rapide de la production

set -e

echo "🧪 Tests Production - PharmaBot"
echo "================================"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

FRONTEND_URL="https://pharmabot-vidal-assistant.netlify.app"
BACKEND_URL="https://pharmabot-olwu.onrender.com"

echo -e "\n${BLUE}1. Test Frontend${NC}"
if curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" | grep -q "200"; then
    echo -e "${GREEN}✅ Frontend accessible${NC}"
else
    echo -e "${RED}❌ Frontend inaccessible${NC}"
    exit 1
fi

echo -e "\n${BLUE}2. Test Backend Health${NC}"
echo "   Tentative de réveil du backend (peut prendre 30s)..."
HEALTH_STATUS=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/api/health" --max-time 40)
HTTP_CODE=$(echo "$HEALTH_STATUS" | tail -n1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Backend actif${NC}"
    echo "$HEALTH_STATUS" | head -n-1 | python3 -m json.tool 2>/dev/null || echo "$HEALTH_STATUS"
elif [ "$HTTP_CODE" = "000" ]; then
    echo -e "${YELLOW}⏳ Backend en démarrage... Réessayez dans 1 minute${NC}"
else
    echo -e "${YELLOW}⚠️  Backend: HTTP $HTTP_CODE${NC}"
    echo "   Vérifiez l'URL ou le déploiement Render"
fi

echo -e "\n${BLUE}3. Test CORS${NC}"
CORS_TEST=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Origin: ${FRONTEND_URL}" \
    -H "Access-Control-Request-Method: POST" \
    -X OPTIONS "${BACKEND_URL}/api/chat" \
    --max-time 10)

if [ "$CORS_TEST" = "200" ] || [ "$CORS_TEST" = "204" ]; then
    echo -e "${GREEN}✅ CORS configuré${NC}"
else
    echo -e "${YELLOW}⚠️  CORS: HTTP $CORS_TEST (peut être normal si backend endormi)${NC}"
fi

echo -e "\n${BLUE}4. GitHub Actions${NC}"
echo "   Vérifiez: https://github.com/Xprriacst/pharmabot/actions"

echo -e "\n${BLUE}5. Logs en direct${NC}"
echo "   Frontend: https://app.netlify.com/sites/pharmabot-vidal-assistant"
echo "   Backend: https://dashboard.render.com"

echo -e "\n${GREEN}Tests terminés !${NC}"
echo -e "\n💡 Pour tests complets Playwright:"
echo "   cd frontend && npx playwright test production.spec.ts"
