# 🔧 Troubleshooting Backend Render

## ❌ Erreur 502 Bad Gateway

**URL**: https://pharmabot-olwu.onrender.com  
**Statut**: Service déployé mais ne démarre pas

## ✅ Étapes de Résolution

### 1. Vérifier les Logs Render
```
https://dashboard.render.com/web/srv-YOUR-SERVICE-ID/logs
```

Cherchez les erreurs:
- `OPENAI_API_KEY not configured`
- `ModuleNotFoundError`
- Erreurs Python/FastAPI

### 2. Vérifier les Variables d'Environnement

Sur Render Dashboard → Environment → Variables requises:

```bash
OPENAI_API_KEY=sk-your-key-here          # ⚠️ OBLIGATOIRE
CHROMA_DB_PATH=/opt/render/project/src/data/chroma_db
SCRAPING_CACHE_PATH=/opt/render/project/src/data/cache
APP_NAME=PharmaBot
APP_VERSION=1.0.0
DEBUG=False
ALLOWED_ORIGINS=https://pharmabot-vidal-assistant.netlify.app
```

### 3. Vérifier le Disque Persistant

- **Name**: pharmabot-data
- **Mount Path**: `/opt/render/project/src/data`
- **Size**: 1 GB

### 4. Vérifier la Configuration Build

**Build Command**:
```bash
pip install -r requirements.txt && python -m spacy download fr_core_news_sm
```

**Start Command**:
```bash
bash start.sh
```

OU directement:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 5. Tester Localement

```bash
cd backend
source venv/bin/activate

# Simuler l'environnement Render
export PORT=8000
export OPENAI_API_KEY=your-key
export CHROMA_DB_PATH=./data/chroma_db

# Tester le démarrage
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 6. Vérifier render.yaml

Le fichier `backend/render.yaml` doit contenir:

```yaml
services:
  - type: web
    name: pharmabot-backend
    env: python
    region: frankfurt
    plan: free
    branch: main
    buildCommand: "pip install -r requirements.txt && python -m spacy download fr_core_news_sm"
    startCommand: "bash start.sh"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.18
      - key: OPENAI_API_KEY
        sync: false  # À configurer manuellement
    disk:
      name: pharmabot-data
      mountPath: /opt/render/project/src/data
      sizeGB: 1
```

## 🐛 Erreurs Communes

### Erreur: "OPENAI_API_KEY not configured"
**Solution**: Ajouter la clé API dans Environment Variables sur Render

### Erreur: "No module named 'app'"
**Solution**: Vérifier que le Root Directory est bien `backend`

### Erreur: "Port already in use"
**Solution**: Utiliser `$PORT` dans la commande start

### Erreur: "ChromaDB: no such table"
**Solution**: 
1. Charger des données de démo
2. OU accepter que la DB soit vide au premier démarrage

## 📊 Commandes Utiles

### Forcer un Redéploiement
```bash
git commit --allow-empty -m "Trigger Render redeploy"
git push origin main
```

### Tester l'API Health
```bash
# Attendre 30s pour cold start
curl https://pharmabot-olwu.onrender.com/api/health
```

### Charger les Données de Démo (via API)
```bash
curl -X POST https://pharmabot-olwu.onrender.com/api/load-demo-data
```

## 🎯 Checklist Déploiement

- [ ] Variables d'environnement configurées
- [ ] OPENAI_API_KEY ajoutée
- [ ] Disque persistant attaché
- [ ] Build command correcte
- [ ] Start command correcte
- [ ] Logs sans erreur
- [ ] Health endpoint répond 200

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Logs en direct**: Dashboard Render → Logs tab

---

**Prochaine étape**: Une fois corrigé, redéployer et tester avec:
```bash
./scripts/test_production.sh
```
