import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MeddisparScraper:
    """Scraper pour extraire les données de Meddispar"""
    
    BASE_URL = "https://www.meddispar.fr"
    
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
    
    async def get_medication_links(self) -> List[Dict[str, str]]:
        """Récupère les liens vers les médicaments"""
        logger.info("Fetching medication links from Meddispar...")
        
        html = await self.fetch_page(self.BASE_URL)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        medications = []
        
        # Find medication links (à adapter selon la structure réelle du site)
        med_links = soup.find_all('a', href=lambda x: x and '/medicament' in x.lower())
        
        for link in med_links:
            title = link.get_text(strip=True)
            url = link.get('href')
            
            if url and not url.startswith('http'):
                url = self.BASE_URL + url
            
            if title and url and url not in [m['url'] for m in medications]:
                medications.append({
                    'title': title,
                    'url': url,
                    'source_type': 'meddispar',
                    'category': 'medicament'
                })
        
        logger.info(f"Found {len(medications)} medication links")
        return medications
    
    async def scrape_medication_page(self, url: str, title: str) -> Dict:
        """Scrape une page de médicament spécifique"""
        logger.info(f"Scraping: {title}")
        
        html = await self.fetch_page(url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract main content
        content_parts = []
        
        # Find main content area
        main_content = soup.find('article') or soup.find('div', class_='content') or soup.find('main')
        
        if main_content:
            # Extract relevant information
            for element in main_content.find_all(['p', 'li', 'h2', 'h3', 'div']):
                text = element.get_text(strip=True)
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
            'source_type': 'meddispar',
            'category': 'medicament'
        }
    
    async def scrape_all(self, max_pages: int = None) -> List[Dict]:
        """Scrape toutes les pages de Meddispar"""
        try:
            # Get all medication links
            medications = await self.get_medication_links()
            
            if max_pages:
                medications = medications[:max_pages]
            
            documents = []
            
            # Scrape each medication
            for i, med in enumerate(medications):
                if i > 0 and i % 10 == 0:
                    logger.info(f"Progress: {i}/{len(medications)} pages scraped")
                
                doc = await self.scrape_medication_page(med['url'], med['title'])
                if doc:
                    documents.append(doc)
                
                # Rate limiting
                await asyncio.sleep(settings.REQUEST_DELAY)
            
            logger.info(f"✅ Scraped {len(documents)} documents from Meddispar")
            return documents
            
        finally:
            await self.close_session()
