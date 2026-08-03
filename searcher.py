import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import time
from typing import List, Dict
from config import Config

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_web_candidates(max_results_per_query: int = 8) -> List[Dict[str, str]]:
    """Performs DuckDuckGo web searches for target training/scholarship queries."""
    ddgs = DDGS()
    candidates = []
    seen_urls = set()

    for query in Config.SEARCH_QUERIES:
        try:
            results = ddgs.text(query, max_results=max_results_per_query)
            for res in results:
                url = res.get('href') or res.get('link')
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                candidates.append({
                    'title': res.get('title', ''),
                    'url': url,
                    'snippet': res.get('body', '')
                })
        except Exception as e:
            print(f"[Searcher] Aviso ao buscar query '{query}': {e}")
        time.sleep(1) # Respeita limite de requisicoes

    return candidates

def fetch_page_content(url: str, timeout: int = 4) -> str:
    """Fetches text content from a web page URL."""
    if url.lower().endswith('.pdf'):
        return "" # Ignora download de PDF bruto pelo requests
        
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts, estilizacao e elementos irrelevantes
            for element in soup(["script", "style", "nav", "footer", "header", "form", "svg"]):
                element.extract()
                
            text = soup.get_text(separator=' ', strip=True)
            return text[:3000]
    except Exception:
        pass
    return ""
