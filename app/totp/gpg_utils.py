import shlex
import os
import subprocess
from threading import Lock


FILE:str = os.getenv("SECRET_FILE")
assert(FILE is not None)
ENCRYPTED_FILE: str = f'{FILE}.gpg'
PASSPHRASE: str = os.getenv("SECRET_PASSPHRASE")
assert(PASSPHRASE is not None)


def run_cmd(cmd: str) -> None:
    process = subprocess.Popen(shlex.split(cmd))
    process.wait()
mtx = Lock()
def decrypt_secret() -> None:
    mtx.acquire()
    run_cmd(f"gpg --passphrase {PASSPHRASE} -o {FILE} -d --batch {ENCRYPTED_FILE}")
    os.remove(ENCRYPTED_FILE)
    mtx.release()

def encrypt_secret() -> None:
    mtx.acquire()
    run_cmd(f"gpg --passphrase {PASSPHRASE} -o {ENCRYPTED_FILE} -c --batch {FILE}")
    os.remove(FILE)
    mtx.release()

