# PharmaBot - Assistant IA pour Pharmaciens

## Description
Assistant conversationnel spécialisé pour les pharmaciens, entraîné exclusivement sur les bases de données officielles :
- **Vidal** : Base de données des médicaments
- **Meddispar** : Médicaments disponibles en pharmacie

## Architecture
- **Frontend** : React + TypeScript + TailwindCSS + shadcn/ui
- **Backend** : FastAPI (Python)
- **RAG System** : LangChain + ChromaDB pour recherche vectorielle
- **Scraping** : BeautifulSoup4 + Selenium pour extraction des données
- **LLM** : OpenAI GPT-4 ou modèle local compatible

## Fonctionnalités
- Chat contextuel basé sur les sources officielles
- Recherche dans la base Vidal et Meddispar
- Citations des sources pour chaque réponse
- Interface moderne et responsive
- Historique des conversations
- Export des réponses en PDF

## Installation

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python -m spacy download fr_core_news_sm
```

### Frontend
```bash
cd frontend
npm install
```

## Configuration
Créer un fichier `.env` dans le dossier backend :
```
OPENAI_API_KEY=votre_clé_api
CHROMA_DB_PATH=./data/chroma_db
SCRAPING_CACHE_PATH=./data/cache
```

## Utilisation

### Lancer le scraping (première fois)
```bash
cd backend
python scripts/scrape_data.py
```

### Démarrer le backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Démarrer le frontend
```bash
cd frontend
npm run dev
```

L'application sera accessible sur http://localhost:5173

## Avertissement Légal
Cet assistant est un outil d'aide à la décision. Il ne remplace pas l'expertise professionnelle d'un pharmacien diplômé. Toujours vérifier les informations critiques dans les sources officielles.
