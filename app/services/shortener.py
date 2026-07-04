import string
import random

BASE62 = string.digits + string.ascii_letters

def encode_base62(num:int) -> str:
    if num == 0:
        return BASE62[0]
    
    base = len(BASE62)
    chars = []

    while num > 0:
        num, rem = divmod(num, base)
        chars.append(BASE62[rem])

    return ''.join(reversed(chars))

def generate_code(length:int = 7) -> str:
    return ''.join(random.choices(BASE62, k=length))