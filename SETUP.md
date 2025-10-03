# Guide d'Installation - PharmaBot

## Prérequis

- Python 3.10 ou supérieur
- Node.js 18 ou supérieur
- Une clé API OpenAI

## Installation Backend

### 1. Créer l'environnement virtuel Python

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# OU
venv\Scripts\activate  # Sur Windows
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
python -m spacy download fr_core_news_sm
```

### 3. Configuration

Créer un fichier `.env` dans le dossier `backend` :

```bash
cp .env.example .env
```

Éditer le fichier `.env` et ajouter votre clé API OpenAI :

```
OPENAI_API_KEY=sk-votre-clé-api-ici
```

### 4. Collecter les données (IMPORTANT)

**Cette étape est cruciale** - Elle récupère les données officielles et les indexe :

```bash
cd backend
python scripts/scrape_data.py
```

⏱️ **Temps estimé** : 10-30 minutes selon le nombre de pages

📊 **Progression** : Le script affiche le nombre de documents collectés en temps réel

⚠️ **Note** : Pour la première utilisation, limitez le scraping (max_pages=50) pour tester rapidement.

### 5. Démarrer le serveur backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Le backend sera accessible sur : http://localhost:8000

Documentation API : http://localhost:8000/docs

## Installation Frontend

### 1. Installer les dépendances

```bash
cd frontend
npm install
```

### 2. Configuration (optionnel)

Créer un fichier `.env` dans le dossier `frontend` :

```bash
cp .env.example .env
```

Le fichier par défaut pointe vers http://localhost:8000/api

### 3. Démarrer le serveur de développement

```bash
npm run dev
```

Le frontend sera accessible sur : http://localhost:5173

## Vérification de l'installation

### 1. Tester le backend

```bash
curl http://localhost:8000/api/health
```

Résultat attendu :
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "app": "PharmaBot",
  "version": "1.0.0"
}
```

### 2. Vérifier la base de données

```bash
curl http://localhost:8000/api/search/stats
```

Doit afficher le nombre de documents indexés.

### 3. Tester le frontend

Ouvrir http://localhost:5173 dans votre navigateur

## Dépannage

### Erreur : "No documents in database"

➡️ Vous devez d'abord exécuter le script de scraping :
```bash
python scripts/scrape_data.py
```

### Erreur : "OpenAI API key not found"

➡️ Vérifiez que votre clé API est correctement configurée dans `.env`

### Erreur : Port déjà utilisé

➡️ Changez le port dans les commandes :
```bash
# Backend
uvicorn app.main:app --reload --port 8001

# Frontend (modifier vite.config.ts)
```

### Le scraping échoue

➡️ Vérifications :
- Connexion internet stable
- Les sites Vidal et Meddispar sont accessibles
- Augmenter `REQUEST_DELAY` dans `.env` si vous êtes bloqué

## Structure des Données

Les données collectées sont stockées dans :

```
backend/data/
├── chroma_db/        # Base vectorielle ChromaDB
└── cache/            # Cache des pages scrapées
```

## Performance

- **Temps de réponse** : 2-5 secondes
- **Précision** : Basée uniquement sur les sources officielles
- **Langues** : Français
- **Sources** : Vidal + Meddispar

## Mise en Production

### Backend

```bash
# Utiliser Gunicorn avec Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Frontend

```bash
npm run build
# Les fichiers sont dans frontend/dist/
```

Déployer sur Vercel, Netlify, ou tout hébergeur statique.

## Avertissement Légal

⚠️ **IMPORTANT** : Cet outil est un assistant d'aide à la décision pour professionnels de santé. Il ne remplace en aucun cas :
- L'expertise d'un pharmacien diplômé
- Une consultation médicale
- La vérification dans les sources officielles pour toute décision critique

## Support

Pour toute question ou problème :
1. Vérifier les logs du backend et frontend
2. Consulter la documentation API : http://localhost:8000/docs
3. Vérifier que les données sont bien indexées

## Licence

Cet outil utilise des données publiques de Vidal et Meddispar. Respectez les conditions d'utilisation de ces sources.
