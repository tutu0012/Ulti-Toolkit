import string
import random

class Generator:
    def generate(self, level, length, use_symbols, symbols_count):
        if level < 1 or level > 5:
            raise ValueError("Level must be between 1 and 5")
        
        char_pool = string.ascii_lowercase
        if level >= 2:
            char_pool += string.ascii_uppercase
        if level >= 3:
            char_pool += string.digits
        if level >= 4 and use_symbols:
            char_pool += "!@#$%^&*()_+-=[]{}|;:,.<>/?"

        if use_symbols and symbols_count > 0:
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>/?"
            if symbols_count > length:
                raise ValueError("symbols_count can't be greater than total length")
            
            password_chars = random.choices(symbols, k=symbols_count)
            password_chars += random.choices(char_pool, k=length - symbols_count)
            random.shuffle(password_chars)
            return ''.join(password_chars)
        else:
            return ''.join(random.choices(char_pool, k=length))