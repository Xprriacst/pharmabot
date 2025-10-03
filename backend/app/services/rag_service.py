import sys
import uuid
from typing import List, Dict, Optional

# Ensure chromadb uses pysqlite3 on macOS to avoid sqlite segmentation faults
try:  # pragma: no cover - best effort fallback
    import pysqlite3  # type: ignore

    sys.modules["sqlite3"] = pysqlite3
    sys.modules["sqlite3.dbapi2"] = pysqlite3
except ImportError:
    pass

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from app.config import settings
import chromadb

class RAGService:
    def __init__(self):
        # Lazy initialization - clients created on first use
        self._embeddings = None
        self._llm = None
        self._vectorstore = None
        self._initialized = False
        
        # Session memory storage
        self.sessions = {}
        
    def _ensure_initialized(self):
        """Lazy initialization of OpenAI and Chroma clients"""
        if self._initialized:
            return
        
        if not settings.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not configured. Please set it in your .env file or environment variables."
            )
        
        self._embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self._llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize ChromaDB with new API
        chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH
        )
        
        self._vectorstore = Chroma(
            client=chroma_client,
            collection_name="pharmabot_knowledge",
            embedding_function=self._embeddings,
        )
        
        self._initialized = True
    
    @property
    def embeddings(self):
        self._ensure_initialized()
        return self._embeddings
    
    @property
    def llm(self):
        self._ensure_initialized()
        return self._llm
    
    @property
    def vectorstore(self):
        self._ensure_initialized()
        return self._vectorstore
    
    @property
    def qa_prompt(self):
        """Custom prompt for pharmaceutical context"""
        return PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template="""Tu es un assistant IA spécialisé pour les pharmaciens. Tu dois répondre uniquement en te basant sur les informations officielles du Vidal et de Meddispar fournies ci-dessous.

RÈGLES IMPORTANTES:
1. Réponds UNIQUEMENT avec les informations contenues dans le contexte fourni
2. Si tu ne trouves pas l'information dans le contexte, dis clairement "Je n'ai pas trouvé cette information dans les bases Vidal ou Meddispar"
3. Cite toujours tes sources (Vidal ou Meddispar)
4. Utilise un langage professionnel adapté aux pharmaciens
5. En cas de doute, recommande de consulter directement les bases officielles
6. N'invente JAMAIS d'informations médicales
7. Rappelle que cet assistant est un outil d'aide à la décision et ne remplace pas le jugement professionnel

Contexte des bases officielles:
{context}

Historique de conversation:
{chat_history}

Question du pharmacien: {question}

Réponse basée uniquement sur les sources officielles:"""
        )
    
    async def generate_response(
        self,
        query: str,
        conversation_history: Optional[List] = None,
        session_id: Optional[str] = None
    ) -> Dict:
        """Generate response using RAG"""
        
        # Create or get session
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
        
        memory = self.sessions[session_id]
        
        # Create retrieval chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": settings.TOP_K_RESULTS}
            ),
            memory=memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": self.qa_prompt}
        )
        
        # Generate response
        result = await qa_chain.ainvoke({"question": query})
        
        # Format sources
        sources = []
        for doc in result.get("source_documents", []):
            sources.append({
                "title": doc.metadata.get("title", "Document"),
                "content": doc.page_content[:300] + "...",
                "url": doc.metadata.get("url", ""),
                "source_type": doc.metadata.get("source_type", "unknown"),
                "relevance_score": doc.metadata.get("score", 0.0)
            })
        
        return {
            "response": result["answer"],
            "sources": sources,
            "session_id": session_id,
            "tokens_used": None  # Can be tracked with callbacks
        }
    
    async def search_documents(
        self,
        query: str,
        source_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Search documents in the vector store"""
        
        # Build filter
        filter_dict = {}
        if source_type:
            filter_dict["source_type"] = source_type
        
        # Perform similarity search
        docs = self.vectorstore.similarity_search_with_score(
            query,
            k=limit,
            filter=filter_dict if filter_dict else None
        )
        
        results = []
        for doc, score in docs:
            results.append({
                "title": doc.metadata.get("title", "Document"),
                "content": doc.page_content,
                "url": doc.metadata.get("url", ""),
                "source_type": doc.metadata.get("source_type", "unknown"),
                "relevance_score": float(1 - score)  # Convert distance to similarity
            })
        
        return results
    
    async def get_stats(self) -> Dict:
        """Get database statistics"""
        collection = self.vectorstore._collection
        count = collection.count()
        
        return {
            "total_documents": count,
            "embedding_model": settings.EMBEDDING_MODEL,
            "llm_model": settings.LLM_MODEL,
            "chunk_size": settings.CHUNK_SIZE,
            "sources": ["Vidal", "Meddispar"]
        }
    
    def clear_session(self, session_id: str):
        """Clear conversation memory for a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        texts = []
        metadatas = []
        
        for doc in documents:
            chunks = text_splitter.split_text(doc["content"])
            for chunk in chunks:
                texts.append(chunk)
                metadatas.append({
                    "title": doc.get("title", ""),
                    "url": doc.get("url", ""),
                    "source_type": doc.get("source_type", "unknown"),
                    "category": doc.get("category", "")
                })
        
        self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
