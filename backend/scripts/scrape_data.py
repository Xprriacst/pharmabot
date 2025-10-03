#!/usr/bin/env python3
"""
Script to scrape data from Vidal and Meddispar and index it in ChromaDB
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.scraper_vidal import VidalScraper
from app.services.scraper_meddispar import MeddisparScraper
from app.services.rag_service import RAGService
from app.config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main scraping function"""
    logger.info("🚀 Starting data scraping process...")
    logger.info(f"📁 Data will be stored in: {settings.CHROMA_DB_PATH}")
    
    all_documents = []
    
    # Scrape Vidal
    logger.info("\n" + "="*60)
    logger.info("📚 SCRAPING VIDAL")
    logger.info("="*60)
    try:
        vidal_scraper = VidalScraper()
        vidal_docs = await vidal_scraper.scrape_all(max_pages=50)  # Limit for testing
        all_documents.extend(vidal_docs)
        logger.info(f"✅ Vidal: {len(vidal_docs)} documents collected")
    except Exception as e:
        logger.error(f"❌ Error scraping Vidal: {e}")
    
    # Scrape Meddispar
    logger.info("\n" + "="*60)
    logger.info("💊 SCRAPING MEDDISPAR")
    logger.info("="*60)
    try:
        meddispar_scraper = MeddisparScraper()
        meddispar_docs = await meddispar_scraper.scrape_all(max_pages=50)  # Limit for testing
        all_documents.extend(meddispar_docs)
        logger.info(f"✅ Meddispar: {len(meddispar_docs)} documents collected")
    except Exception as e:
        logger.error(f"❌ Error scraping Meddispar: {e}")
    
    # Index documents
    if all_documents:
        logger.info("\n" + "="*60)
        logger.info("🔍 INDEXING DOCUMENTS")
        logger.info("="*60)
        logger.info(f"Total documents to index: {len(all_documents)}")
        
        try:
            rag_service = RAGService()
            rag_service.add_documents(all_documents)
            logger.info("✅ Documents successfully indexed in ChromaDB")
            
            # Show stats
            stats = await rag_service.get_stats()
            logger.info(f"\n📊 Database Statistics:")
            logger.info(f"   - Total documents: {stats['total_documents']}")
            logger.info(f"   - Embedding model: {stats['embedding_model']}")
            logger.info(f"   - LLM model: {stats['llm_model']}")
            
        except Exception as e:
            logger.error(f"❌ Error indexing documents: {e}")
    else:
        logger.warning("⚠️  No documents collected")
    
    logger.info("\n" + "="*60)
    logger.info("✅ SCRAPING COMPLETE")
    logger.info("="*60)

if __name__ == "__main__":
    asyncio.run(main())
