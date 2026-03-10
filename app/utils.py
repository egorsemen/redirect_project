import string
import random

def create_random_code(chars=string.ascii_letters + string.digits, size=6):
    """Генерирует случайную строку из 6 символов (буквы и цифры)"""
    return "".join(random.choice(chars) for _ in range(size))