# Guide de Déploiement PharmaBot

## ✅ Frontend Déjà Déployé

**URL** : https://pharmabot-vidal-assistant.netlify.app

## 🚀 Déployer le Backend sur Render

### Étape 1 : Créer un compte Render

1. Allez sur https://render.com
2. Créez un compte ou connectez-vous
3. Connectez votre compte GitHub

### Étape 2 : Créer un nouveau Web Service

1. Cliquez sur **"New +"** → **"Web Service"**
2. Connectez votre repository : `Xprriacst/pharmabot`
3. Configurez le service :

**Configuration de base :**
- Name: `pharmabot-backend`
- Region: `Frankfurt (EU Central)`
- Branch: `main`
- Root Directory: `backend`
- Runtime: `Python 3`
- Build Command: `pip install -r requirements.txt && python -m spacy download fr_core_news_sm`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Plan :**
- Sélectionnez **Free** (suffisant pour commencer)

### Étape 3 : Variables d'environnement

Dans l'onglet **Environment**, ajoutez ces variables :

```
OPENAI_API_KEY=votre-clé-api-openai-ici

CHROMA_DB_PATH=/opt/render/project/src/data/chroma_db
SCRAPING_CACHE_PATH=/opt/render/project/src/data/cache
APP_NAME=PharmaBot
APP_VERSION=1.0.0
DEBUG=False
ALLOWED_ORIGINS=https://pharmabot-vidal-assistant.netlify.app
```

### Étape 4 : Ajouter un disque persistant

1. Dans l'onglet **Disks**, cliquez sur **"Add Disk"**
2. Configurez :
   - Name: `pharmabot-data`
   - Mount Path: `/opt/render/project/src/data`
   - Size: `1 GB` (gratuit)

### Étape 5 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Attendez la fin du build (5-10 minutes)
3. Une fois terminé, vous aurez une URL type : `https://pharmabot-backend.onrender.com`

### Étape 6 : Configurer le Frontend

Une fois le backend déployé, mettez à jour la variable d'environnement du frontend sur Netlify :

1. Allez sur https://app.netlify.com/sites/pharmabot-vidal-assistant
2. **Site settings** → **Environment variables**
3. Ajoutez :
   ```
   VITE_API_URL=https://votre-backend.onrender.com/api
   ```
4. Redéployez le frontend (Build & Deploy → Trigger deploy)

### Étape 7 : Charger les données initiales

Le backend chargera automatiquement les données de démonstration au premier démarrage via le script `load_demo_data.py`.

## 🧪 Tester l'Application

Une fois tout déployé :

1. **Frontend** : https://pharmabot-vidal-assistant.netlify.app
2. **Backend API** : https://votre-backend.onrender.com/api/health
3. **API Docs** : https://votre-backend.onrender.com/docs

## ⚠️ Limitations du Plan Gratuit Render

- Le service s'endort après 15 minutes d'inactivité
- Premier appel après inactivité : ~30 secondes de démarrage
- Pour éviter cela : passer au plan payant ($7/mois)

## 🎯 Alternative : Déploiement Local

Si vous préférez tester en local :

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm run dev
```

Accès : http://localhost:5174
