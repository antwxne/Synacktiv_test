import shlex
import os
import subprocess


PASSPHRASE: str = os.getenv("SECRET_PASSPHRASE")
assert PASSPHRASE is not None
SECRETS_FOLDER: str = "./secrets_folder"


def run_cmd(cmd: str) -> None:
    process = subprocess.Popen(shlex.split(cmd))
    process.wait()


def decrypt_secret(filepath: str) -> None:
    run_cmd(f"gpg --passphrase {PASSPHRASE} -o {filepath} -d --batch {filepath}.gpg")


def encrypt_secret(filepath: str) -> None:
    run_cmd(f"gpg --passphrase {PASSPHRASE} -o {filepath}.gpg -c --batch {filepath}")
