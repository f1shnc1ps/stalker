import re
from typing import Dict
from phantom.utils.validators import PhoneValidator

class PhoneRecon:
    """Phone number reconnaissance"""
    
    def __init__(self):
        self.validator = PhoneValidator()
    
    def scan(self, phone: str) -> Dict:
        """Full phone scan"""
        results = {'phone': phone}
        validation = self.validator.validate_phone(phone)
        results.update(validation)
        
        if results.get('valid'):
            clean = results['clean']
            results['truecaller'] = f'https://www.truecaller.com/search/{clean}'
            results['numverify'] = f'https://numverify.com/?phone={clean}'
        
        return results
