import re
from typing import Dict
from phantom.utils.api import IPGeolocation, APIClient
from phantom.utils.validators import IPValidator
import os

class IPRecon:
    """IP address reconnaissance"""
    
    def __init__(self, shodan_key: str = None):
        self.geoloc = IPGeolocation()
        self.client = APIClient()
        self.validator = IPValidator()
        self.shodan_key = shodan_key or os.getenv('SHODAN_API_KEY')
    
    def scan(self, ip: str) -> Dict:
        """Full IP reconnaissance"""
        results = {
            'ip': ip,
            'valid': self.validator.validate_ip(ip),
            'geolocation': {},
            'reputation': {},
            'services': {},
            'dns': {}
        }
        
        if not results['valid']:
            return results
        
        # Geolocation
        results['geolocation'] = self.geoloc.ipinfo(ip)
        
        # Reputation checks
        results['reputation']['abuseipdb'] = self.geoloc.abuseipdb(ip)
        results['reputation']['tor'] = self.geoloc.tor_exit_check(ip)
        
        # Services (Shodan)
        if self.shodan_key:
            results['services'] = self.geoloc.shodan_lookup(ip, self.shodan_key)
        
        # Reverse DNS
        results['dns'] = self.geoloc.reverse_dns(ip)
        
        return results
