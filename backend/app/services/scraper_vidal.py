import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import time
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VidalScraper:
    """Scraper pour extraire les données du Vidal"""
    
    BASE_URL = "https://www.vidal.fr"
    MALADIES_URL = "https://www.vidal.fr/maladies/chez-adulte.html"
    
    def __init__(self):
        self.headers = {
            "User-Agent": settings.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        }
        self.session = None
    
    async def init_session(self):
        """Initialize aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    async def fetch_page(self, url: str, retries: int = 3) -> str:
        """Fetch a page with retry logic"""
        await self.init_session()
        
        for attempt in range(retries):
            try:
                async with self.session.get(url, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        logger.warning(f"Status {response.status} for {url}")
                        
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(settings.REQUEST_DELAY * (attempt + 1))
        
        return None
    
    async def get_disease_categories(self) -> List[Dict[str, str]]:
        """Récupère la liste des catégories de maladies"""
        logger.info("Fetching disease categories from Vidal...")
        
        html = await self.fetch_page(self.MALADIES_URL)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        categories = []
        
        # Find all disease links
        disease_links = soup.find_all('a', href=lambda x: x and '/maladies/' in x)
        
        for link in disease_links:
            title = link.get_text(strip=True)
            url = link.get('href')
            
            if url and not url.startswith('http'):
                url = self.BASE_URL + url
            
            if title and url and url not in [c['url'] for c in categories]:
                categories.append({
                    'title': title,
                    'url': url,
                    'source_type': 'vidal',
                    'category': 'maladie'
                })
        
        logger.info(f"Found {len(categories)} disease categories")
        return categories
    
    async def scrape_disease_page(self, url: str, title: str) -> Dict:
        """Scrape une page de maladie spécifique"""
        logger.info(f"Scraping: {title}")
        
        html = await self.fetch_page(url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract main content
        content_parts = []
        
        # Find article or main content
        main_content = soup.find('article') or soup.find('div', class_='content')
        
        if main_content:
            # Extract paragraphs
            for p in main_content.find_all(['p', 'li', 'h2', 'h3']):
                text = p.get_text(strip=True)
                if text and len(text) > 20:
                    content_parts.append(text)
        
        content = "\n\n".join(content_parts)
        
        if not content:
            logger.warning(f"No content extracted for {title}")
            return None
        
        return {
            'title': title,
            'content': content,
            'url': url,
            'source_type': 'vidal',
            'category': 'maladie'
        }
    
    async def scrape_all(self, max_pages: int = None) -> List[Dict]:
        """Scrape toutes les pages du Vidal"""
        try:
            # Get all categories
            categories = await self.get_disease_categories()
            
            if max_pages:
                categories = categories[:max_pages]
            
            documents = []
            
            # Scrape each category
            for i, category in enumerate(categories):
                if i > 0 and i % 10 == 0:
                    logger.info(f"Progress: {i}/{len(categories)} pages scraped")
                
                doc = await self.scrape_disease_page(category['url'], category['title'])
                if doc:
                    documents.append(doc)
                
                # Rate limiting
                await asyncio.sleep(settings.REQUEST_DELAY)
            
            logger.info(f"✅ Scraped {len(documents)} documents from Vidal")
            return documents
            
        finally:
            await self.close_session()
