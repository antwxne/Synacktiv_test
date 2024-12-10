import json
import hashlib
import os
from .register_model import Register
from .gpg_utils import SECRETS_FOLDER, encrypt_secret, decrypt_secret
from datetime import datetime

class UserDoesNotExist(ValueError):
    def __init__(self, *args):
        super().__init__(*args)


def get_time_format() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M")

def auth_controller(user: str, password: str) -> bool:
    file_path: str = f"{SECRETS_FOLDER}/{user}"
    decrypt_secret(file_path)
    user_secret: str = ""
    with open(file_path, "r") as f:
        user_secret = f.read()
    if user_secret == "": raise UserDoesNotExist(user)
    time: str = get_time_format()
    # time: str = "20220108-1628"

    concatened_str: str = user_secret+time
    current_password = hashlib.sha256(concatened_str.encode()).hexdigest()[:16:]
    return  current_password == password
