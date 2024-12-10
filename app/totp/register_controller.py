import json
import os
from .register_model import Register
from .gpg_utils import FILE, encrypt_secret, decrypt_secret

def register_controller(user: Register) -> None:
    decrypt_secret()
    with open(FILE, "rw") as f:
        content: dict[str, str] = json.load(f)
        content[user.user] = user.secret
        json.dump(content, f)
    encrypt_secret()
