import requests
import socket
import time
from typing import Dict, Optional
import os

class APIClient:
    """Unified API handler with rate limiting"""
    
    def __init__(self, timeout: int = 5, retries: int = 2):
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get(self, url: str, **kwargs) -> Optional[Dict]:
        """GET request with retry logic"""
        for attempt in range(self.retries):
            try:
                r = self.session.get(url, timeout=self.timeout, **kwargs)
                try:
                    data = r.json()
                except:
                    data = None
                return {'status': r.status_code, 'data': data, 'text': r.text}
            except requests.Timeout:
                if attempt == self.retries - 1:
                    return {'error': 'timeout'}
                time.sleep(0.5)
            except Exception as e:
                return {'error': str(e)[:100]}
        return None
    
    def head(self, url: str, **kwargs) -> Optional[Dict]:
        """HEAD request for fast status check"""
        try:
            r = self.session.head(url, timeout=self.timeout, allow_redirects=True, **kwargs)
            return {'status': r.status_code, 'url': r.url}
        except requests.Timeout:
            return {'error': 'timeout'}
        except Exception as e:
            return {'error': str(e)[:100]}

class IPGeolocation:
    """IP geolocation and reputation lookups"""
    
    def __init__(self):
        self.client = APIClient()
    
    def ipinfo(self, ip: str) -> Dict:
        """ipinfo.io geolocation lookup"""
        try:
            resp = self.client.get(f'https://ipinfo.io/{ip}/json')
            if resp and resp.get('status') == 200 and resp.get('data'):
                data = resp['data']
                return {
                    'provider': 'ipinfo.io',
                    'country': data.get('country'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'isp': data.get('org'),
                    'coordinates': data.get('loc'),
                    'timezone': data.get('timezone')
                }
        except:
            pass
        return {}
    
    def abuseipdb(self, ip: str) -> Dict:
        """AbuseIPDB reputation check"""
        try:
            headers = {
                'Key': os.getenv('ABUSEIPDB_API_KEY', ''),
                'Accept': 'application/json'
            }
            if not headers['Key']:
                return {}
            
            resp = self.client.get(
                'https://api.abuseipdb.com/api/v2/check',
                params={'ipAddress': ip, 'maxAgeInDays': 90},
                headers=headers
            )
            if resp and resp.get('status') == 200:
                data = resp.get('data', {}).get('data', {})
                return {
                    'provider': 'abuseipdb',
                    'abuse_score': data.get('abuseConfidenceScore'),
                    'total_reports': data.get('totalReports'),
                    'is_whitelisted': data.get('isWhitelisted')
                }
        except:
            pass
        return {}
    
    def shodan_lookup(self, ip: str, api_key: str = None) -> Dict:
        """Shodan service discovery"""
        try:
            key = api_key or os.getenv('SHODAN_API_KEY')
            if not key:
                return {}
            
            resp = self.client.get(
                f'https://api.shodan.io/shodan/host/{ip}',
                params={'key': key}
            )
            if resp and resp.get('status') == 200:
                data = resp.get('data', {})
                ports = data.get('ports', [])
                return {
                    'provider': 'shodan',
                    'open_ports': ports,
                    'services': [f"{p}/tcp" for p in ports],
                    'hostnames': data.get('hostnames', [])
                }
        except:
            pass
        return {}
    
    def tor_exit_check(self, ip: str) -> Dict:
        """Check if IP is Tor exit node"""
        try:
            resp = self.client.get('https://check.torproject.org/torbulkexitlist')
            if resp and resp.get('status') == 200:
                tor_ips = resp.get('text', '').strip().split('\n')
                return {
                    'provider': 'torproject',
                    'is_tor_exit': ip in tor_ips
                }
        except:
            pass
        return {}
    
    def reverse_dns(self, ip: str) -> Dict:
        """Reverse DNS lookup"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return {
                'provider': 'dns',
                'hostname': hostname
            }
        except socket.herror:
            return {'provider': 'dns', 'hostname': None}
        except:
            return {}
