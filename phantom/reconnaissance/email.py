from phantom.utils.api import APIClient
from phantom.utils.validators import EmailValidator
from typing import Dict
import re

class EmailRecon:
    """Email reconnaissance - breach checking, validation, reputation"""
    
    def __init__(self):
        self.client = APIClient()
        self.validator = EmailValidator()
    
    def scan(self, email: str) -> dict:
        """Full email scan"""
        results = {
            'email': email,
            'valid': self.validator.validate_email(email),
            'hibp': {},
            'emailrep': {},
            'smtp': {}
        }
        
        if not results['valid']:
            return results
        
        # Have I Been Pwned
        try:
            resp = self.client.get(
                f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
                headers={'User-Agent': 'PHANTOM-OSINT'}
            )
            if resp and resp.get('status') == 200:
                breaches = resp.get('data', [])
                results['hibp'] = {
                    'found': True,
                    'breach_count': len(breaches),
                    'breaches': [b.get('Name', b) if isinstance(b, dict) else b for b in breaches[:10]]
                }
            else:
                results['hibp'] = {'found': False}
        except:
            results['hibp'] = {'error': 'HIBP check failed'}
        
        # EmailRep reputation check
        try:
            resp = self.client.get(f'https://emailrep.io/{email}')
            if resp and resp.get('status') == 200:
                data = resp.get('data', {})
                results['emailrep'] = {
                    'found': True,
                    'reputation': data.get('reputation', 'unknown'),
                    'fraud_level': data.get('details', {}).get('malicious_activity'),
                    'suspicious_tld': data.get('details', {}).get('suspicious_tld')
                }
        except:
            results['emailrep'] = {'error': 'EmailRep check failed'}
        
        # SMTP validation
        try:
            domain = email.split('@')[1]
            import socket
            mx_records = self.validator.get_mx_records(domain)
            results['smtp'] = {
                'valid': len(mx_records) > 0,
                'mx_records': len(mx_records),
                'mx_hosts': mx_records[:3]
            }
        except:
            results['smtp'] = {'error': 'SMTP validation failed'}
        
        return results
