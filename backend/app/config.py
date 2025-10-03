from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "PharmaBot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API Keys
    OPENAI_API_KEY: str
    
    # Database
    CHROMA_DB_PATH: str = "./data/chroma_db"
    SCRAPING_CACHE_PATH: str = "./data/cache"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Scraping
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    REQUEST_DELAY: int = 2
    MAX_RETRIES: int = 3
    
    # RAG Configuration
    EMBEDDING_MODEL: str = "text-embedding-3-large"
    LLM_MODEL: str = "gpt-4o"  # GPT-4o - Octobre 2025
    LLM_TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 4000
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure directories exist
Path(settings.CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)
Path(settings.SCRAPING_CACHE_PATH).mkdir(parents=True, exist_ok=True)
