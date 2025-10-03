# Architecture Technique - PharmaBot

## Vue d'ensemble

PharmaBot est un assistant conversationnel basé sur l'architecture RAG (Retrieval-Augmented Generation) spécialement conçu pour les pharmaciens.

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   Frontend  │ ───▶ │   Backend    │ ───▶ │  ChromaDB       │
│   React     │      │   FastAPI    │      │  (Vecteurs)     │
└─────────────┘      └──────────────┘      └─────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  OpenAI API  │
                     │  GPT-4       │
                     └──────────────┘
```

## Stack Technique

### Backend (Python)

- **Framework**: FastAPI 
- **LLM**: OpenAI GPT-4 Turbo
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector Store**: ChromaDB
- **RAG Framework**: LangChain
- **Web Scraping**: BeautifulSoup4 + aiohttp
- **NLP**: spaCy (français)

### Frontend (TypeScript)

- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Components**: shadcn/ui (Radix UI)
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Markdown**: react-markdown

## Architecture RAG

### 1. Pipeline de Collecte des Données

```python
Sources → Scraping → Nettoyage → Chunking → Embeddings → ChromaDB
```

**Étapes détaillées:**

1. **Scraping** (`scraper_vidal.py`, `scraper_meddispar.py`)
   - Collecte asynchrone des pages
   - Rate limiting pour respecter les serveurs
   - Cache local pour éviter les requêtes répétées
   - Extraction du contenu pertinent (HTML → Texte)

2. **Chunking** (dans `rag_service.py`)
   ```python
   RecursiveCharacterTextSplitter(
       chunk_size=1000,      # Taille des segments
       chunk_overlap=200,    # Chevauchement pour contexte
   )
   ```

3. **Embeddings**
   - Modèle: `text-embedding-3-small`
   - Dimension: 1536
   - Chaque chunk → vecteur numérique

4. **Indexation ChromaDB**
   - Stockage des vecteurs + métadonnées
   - Recherche par similarité cosinus

### 2. Pipeline de Génération de Réponse

```
Question → Embedding → Recherche Vectorielle → Contexte + Prompt → GPT-4 → Réponse
```

**Workflow:**

1. **Question utilisateur** → Convertie en embedding

2. **Recherche vectorielle**
   ```python
   vectorstore.similarity_search_with_score(
       query,
       k=5,  # Top 5 résultats
       filter={"source_type": "vidal"}  # Optionnel
   )
   ```

3. **Construction du contexte**
   - Les 5 documents les plus pertinents
   - Métadonnées (source, URL, titre)

4. **Prompt Engineering**
   ```
   Tu es un assistant IA spécialisé pour les pharmaciens.
   
   RÈGLES:
   - Réponds UNIQUEMENT avec les informations du contexte
   - Cite tes sources (Vidal ou Meddispar)
   - Si pas d'info: dis-le clairement
   - Ne jamais inventer d'informations médicales
   
   Contexte: {documents pertinents}
   Question: {question utilisateur}
   ```

5. **Génération GPT-4**
   - Temperature: 0.3 (précision vs créativité)
   - Max tokens: 2000
   - Retour avec sources citées

### 3. Système de Mémoire Conversationnelle

```python
ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
```

- Maintient l'historique par session
- Permet le suivi contextuel
- Session ID unique par conversation

## Modèle de Données

### Document dans ChromaDB

```json
{
  "id": "uuid",
  "content": "Texte du document chunké",
  "embedding": [0.123, -0.456, ...],  // 1536 dimensions
  "metadata": {
    "title": "Paracétamol - Indications",
    "url": "https://www.vidal.fr/...",
    "source_type": "vidal",  // ou "meddispar"
    "category": "medicament"
  }
}
```

### API Request/Response

**Chat Request:**
```json
{
  "message": "Quelles sont les indications du paracétamol?",
  "conversation_history": [...],
  "session_id": "uuid-session"
}
```

**Chat Response:**
```json
{
  "response": "Le paracétamol est indiqué pour...",
  "sources": [
    {
      "title": "Paracétamol - Vidal",
      "content": "Extrait...",
      "url": "https://...",
      "source_type": "vidal",
      "relevance_score": 0.92
    }
  ],
  "session_id": "uuid-session",
  "timestamp": "2024-01-15T10:30:00"
}
```

## Sécurité et Contraintes

### Contraintes RAG

1. **Hallucination Prevention**
   - Prompt strict: "UNIQUEMENT les informations du contexte"
   - Temperature basse (0.3)
   - Système de citation obligatoire

2. **Quality Control**
   - Sources officielles uniquement (Vidal + Meddispar)
   - Vérification des métadonnées
   - Avertissement légal systématique

3. **Rate Limiting**
   - Scraping: 2 secondes entre requêtes
   - API OpenAI: Limites du compte

### Sécurité

- **API Key**: Stockée dans `.env`, jamais commitée
- **CORS**: Configuré pour domaines autorisés
- **Validation**: Pydantic pour toutes les entrées
- **Sanitization**: BeautifulSoup pour nettoyage HTML

## Performance

### Optimisations

1. **Scraping Asynchrone**
   - `aiohttp` pour parallélisme
   - Cache local des pages

2. **Vector Search**
   - ChromaDB optimisé pour recherche rapide
   - Index HNSW (Hierarchical Navigable Small World)

3. **Frontend**
   - React lazy loading
   - Debouncing sur recherche
   - Optimistic UI updates

### Métriques Estimées

- **Temps de réponse chat**: 2-5 secondes
- **Recherche vectorielle**: <100ms
- **Scraping initial**: 10-30 minutes
- **Stockage ChromaDB**: ~500MB pour 10k documents

## Évolutions Possibles

### Court terme

- [ ] Export PDF des conversations
- [ ] Historique persistant (base SQL)
- [ ] Multi-utilisateurs avec auth
- [ ] Mode hors-ligne (modèle local)

### Moyen terme

- [ ] Fine-tuning sur données pharmaceutiques
- [ ] Intégration d'autres sources (ANSM, EMA)
- [ ] Recherche multimodale (images de médicaments)
- [ ] API publique avec rate limiting

### Long terme

- [ ] Modèle français spécialisé pharmacie
- [ ] Système de recommandation
- [ ] Détection d'interactions médicamenteuses
- [ ] Intégration logiciels pharmacie (LGO)

## Maintenance

### Mise à jour des données

```bash
# Scraping incrémental
python scripts/scrape_data.py --incremental

# Scraping complet (écrase tout)
python scripts/scrape_data.py --full
```

### Monitoring

- Logs applicatifs: `backend/logs/`
- Métriques OpenAI: Dashboard OpenAI
- Health check: `/api/health`

### Backup

```bash
# ChromaDB
tar -czf backup_$(date +%Y%m%d).tar.gz backend/data/chroma_db/

# Restore
tar -xzf backup_20240115.tar.gz -C backend/data/
```

## Conformité et Légal

⚠️ **Important**: 

- Respecter les CGU de Vidal et Meddispar
- Scraping responsable (rate limiting)
- Données à usage professionnel uniquement
- Avertissement légal visible dans l'UI
- Ne remplace pas l'expertise pharmacienne
- Vérification obligatoire pour décisions critiques

## Support et Debugging

### Logs utiles

```bash
# Backend
tail -f backend/logs/app.log

# Scraping
python scripts/scrape_data.py --verbose

# ChromaDB status
python -c "from app.services.rag_service import RAGService; r=RAGService(); print(r.get_stats())"
```

### Tests

```bash
# Backend
cd backend
pytest tests/

# Frontend
cd frontend
npm test
```

## Ressources

- **LangChain Docs**: https://python.langchain.com/
- **ChromaDB Docs**: https://docs.trychroma.com/
- **OpenAI API**: https://platform.openai.com/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **RAG Pattern**: https://www.pinecone.io/learn/retrieval-augmented-generation/
