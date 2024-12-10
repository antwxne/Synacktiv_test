import json
import hashlib
import os
from .register_model import Register
from .gpg_utils import FILE, encrypt_secret, decrypt_secret
from datetime import datetime

class UserDoesNotExist(ValueError):
    def __init__(self, *args):
        super().__init__(*args)


def get_time_format() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M")

def auth_controller(user: str, password: str) -> bool:
    decrypt_secret()
    content: dict[str, str] = {} 
    with open(FILE, "r") as f:
        content = json.load(f)
    encrypt_secret()
    if user not in content: raise UserDoesNotExist(user)
    user_secret: str = content[user]
    time: str = get_time_format
    current_password = hashlib.sha256(user+time).hexdigest()[:16:]
    return False
    return  current_password == password
