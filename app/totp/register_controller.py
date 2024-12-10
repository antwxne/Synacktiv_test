import json
import os
from .register_model import Register
from .gpg_utils import SECRETS_FOLDER, encrypt_secret, decrypt_secret


def register_controller(user: Register) -> None:
    filepath: str = f"{SECRETS_FOLDER}/{user.user}"
    with open(filepath, "w") as f:
        f.write(user.secret)
    encrypt_secret(filepath)
    os.remove(filepath)
