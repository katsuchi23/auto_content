"""
Text Normalizer Module
Handles text normalization for audio generation
"""

import re
from num2words import num2words

class TextNormalizer:
    def __init__(self):
        self.number_patterns = {
            'integer': r'\b\d+\b',
            'decimal': r'\b\d+\.\d+\b',
            'ordinal': r'\b\d+(st|nd|rd|th)\b',
            'time': r'\b\d{1,2}:\d{2}\b',
            'date': r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            'currency': r'\$\d+(\.\d{2})?',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'fraction': r'\b\d+/\d+\b',
            'hyphen': r'\b\d+(?=-)|-(?=\d+|present\b)',
            'scientific': r'\b\d+\.?\d*\s*x\s*10\^-?\d+\b',  # Scientific notation pattern
            'multiplication': r'\b\d+\.?\d*\s*x\s*\d+\.?\d*\b',  # Simple multiplication pattern
            'power': r'\b\d+\.?\d*\^-?\d+\b'  # Power pattern
        }

    def normalize_numbers(self, text):
        """
        Convert numbers in text to their word representation
        """
        # Handle scientific notation first (e.g., 1.898 x 10^27)
        text = re.sub(self.number_patterns['scientific'],
                     lambda x: self._convert_scientific(x.group()), text)
        
        # Handle simple multiplication (e.g., 2 x 3)
        text = re.sub(self.number_patterns['multiplication'],
                     lambda x: self._convert_multiplication(x.group()), text)
        
        # Handle powers (e.g., 2^3)
        text = re.sub(self.number_patterns['power'],
                     lambda x: self._convert_power(x.group()), text)
        
        # Handle hyphens between numbers or before 'present'
        text = re.sub(self.number_patterns['hyphen'],
                     lambda x: ' until ' if x.group() == '-' else num2words(int(x.group())), text)
        
        # Rest of the existing conversions...
        text = re.sub(self.number_patterns['currency'], 
                     lambda x: self._convert_currency(x.group()), text)
        
        text = re.sub(self.number_patterns['phone'],
                     lambda x: self._convert_phone(x.group()), text)
        
        text = re.sub(self.number_patterns['fraction'],
                     lambda x: self._convert_fraction(x.group()), text)
        
        text = re.sub(self.number_patterns['time'], 
                     lambda x: self._convert_time(x.group()), text)
        
        text = re.sub(self.number_patterns['date'], 
                     lambda x: self._convert_date(x.group()), text)
        
        text = re.sub(self.number_patterns['ordinal'], 
                     lambda x: self._convert_ordinal(x.group()), text)
        
        text = re.sub(self.number_patterns['decimal'], 
                     lambda x: self._convert_decimal(x.group()), text)
        
        text = re.sub(self.number_patterns['integer'], 
                     lambda x: num2words(int(x.group())), text)
        
        return text

    def _convert_scientific(self, text):
        """Convert scientific notation (e.g., 1.898 x 10^27)"""
        # Split into base number and exponent
        base_str, exp_str = text.split('x')
        base = float(base_str.strip())
        exp = int(exp_str.replace('10^', '').strip())
        
        base_words = num2words(base)
        exp_words = num2words(abs(exp))
        
        if exp < 0:
            return f"{base_words} times ten to the negative {exp_words} power"
        else:
            return f"{base_words} times ten to the {exp_words} power"

    def _convert_multiplication(self, text):
        """Convert multiplication (e.g., 2 x 3)"""
        num1, num2 = map(float, text.split('x'))
        return f"{num2words(num1)} times {num2words(num2)}"

    def _convert_power(self, text):
        """Convert power expressions (e.g., 2^3)"""
        base, exp = map(float, text.split('^'))
        exp_words = num2words(abs(exp))
        
        if exp < 0:
            return f"{num2words(base)} to the negative {exp_words} power"
        else:
            return f"{num2words(base)} to the {exp_words} power"

    def _convert_currency(self, text):
        amount = float(text.replace('$', ''))
        dollars = int(amount)
        cents = int((amount - dollars) * 100)
        
        result = num2words(dollars) + ' dollars'
        if cents > 0:
            result += ' and ' + num2words(cents) + ' cents'
        return result

    def _convert_phone(self, text):
        digits = re.sub(r'[-.]', '', text)
        return ' '.join(num2words(int(digit)) for digit in digits)

    def _convert_fraction(self, text):
        num, denom = map(int, text.split('/'))
        return num2words(num) + ' over ' + num2words(denom)

    def _convert_time(self, text):
        hours, minutes = map(int, text.split(':'))
        return f"{num2words(hours)} {'' if hours == 1 else ''} {minutes:02d}"

    def _convert_date(self, text):
        month, day, year = map(int, text.split('/'))
        return f"{num2words(month)} {num2words(day)} {num2words(year)}"

    def _convert_ordinal(self, text):
        number = int(re.search(r'\d+', text).group())
        return num2words(number, ordinal=True)

    def _convert_decimal(self, text):
        return num2words(float(text))