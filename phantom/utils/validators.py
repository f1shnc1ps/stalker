import re
import socket
from typing import List, Dict

class EmailValidator:
    """Email validation and checks"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def get_mx_records(domain: str) -> List[str]:
        """Get MX records for domain"""
        try:
            import dns.resolver
            mx_hosts = []
            try:
                for mx in dns.resolver.resolve(domain, 'MX'):
                    mx_hosts.append(str(mx.exchange))
                return mx_hosts
            except:
                # Fallback to socket
                return []
        except:
            return []

class PhoneValidator:
    """Phone number validation"""
    
    @staticmethod
    def validate_phone(phone: str) -> Dict:
        """Validate phone format"""
        clean = re.sub(r'\D', '', phone)
        
        if len(clean) == 10:
            region = 'US (10-digit)'
        elif len(clean) == 11 and clean.startswith('1'):
            region = 'US (11-digit)'
        elif len(clean) >= 11:
            region = 'International'
        else:
            return {'valid': False}
        
        return {
            'valid': True,
            'region': region,
            'clean': clean,
            'formatted': f"+{clean}" if len(clean) >= 11 else clean
        }

class IPValidator:
    """IP address validation"""
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """Validate IPv4 or IPv6"""
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        ipv6_pattern = r'^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$'
        
        if re.match(ipv4_pattern, ip):
            parts = ip.split('.')
            return all(0 <= int(p) <= 255 for p in parts)
        
        return bool(re.match(ipv6_pattern, ip))
