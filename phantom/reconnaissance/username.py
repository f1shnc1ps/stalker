from concurrent.futures import ThreadPoolExecutor, as_completed
from phantom.databases.sites import SiteDatabase
from phantom.utils.api import APIClient
from typing import Dict
import time

class UsernameRecon:
    """Username reconnaissance across 600+ platforms"""
    
    def __init__(self, username: str, threads: int = 10):
        self.username = username
        self.threads = threads
        self.client = APIClient()
        self.results = {}
    
    def _check_site(self, site: str, config: dict) -> tuple:
        """Single site check"""
        try:
            url = config['url'].replace('{username}', self.username)
            
            if config.get('api'):
                resp = self.client.get(url)
                if resp and resp.get('status') == 200 and resp.get('data'):
                    return (site, {'found': True, 'url': url, 'data': resp.get('data')})
            else:
                resp = self.client.head(url)
                if resp and resp.get('status') == config.get('status', 200):
                    return (site, {'found': True, 'url': url, 'status': resp['status']})
            
            return (site, {'found': False})
        except Exception as e:
            return (site, {'error': str(e)[:50]})
    
    def scan(self) -> Dict:
        """Parallel username scan across all sites"""
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {
                executor.submit(self._check_site, site, cfg): site
                for site, cfg in SiteDatabase.SITES.items()
            }
            
            for future in as_completed(futures):
                site, result = future.result()
                self.results[site] = result
                time.sleep(0.001)
        
        return self.results
