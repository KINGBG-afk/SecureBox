import os
from base64 import urlsafe_b64encode
from os import urandom
from tkinter import messagebox

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Cryptor:
    def __init__(self, path: str, name: str) -> None:
        """Encryption and Decryption of files

        Args:
            path (str): Path to the working env
            name (str): The project's name
        """
        self.path = path
        self.name = name

    def _generate_master_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256 key lenght
            salt=salt,
            iterations=100_000,
            backend=default_backend(),
        )

        return urlsafe_b64encode(kdf.derive(password.encode()))

    def store_password(self, password: str) -> None:
        salt = urandom(16)
        password_hash = self._generate_master_key(password, salt)

        if not os.path.exists(os.path.join(self.path, "password")):
            os.makedirs(os.path.join(self.path, "password"), exist_ok=True)

        with open(os.path.join(self.path, "password", "master_key.txt"), "wb") as f:
            f.write(salt + password_hash)

    def _verify_password(self, password: str) -> bool:
        with open(os.path.join(self.path, "password", "master_key.txt"), "rb") as f:
            data = f.read()
            salt = data[:16]
            stored_pass_hash = data[16:]

        password_hash = self._generate_master_key(password, salt)
        return password_hash == stored_pass_hash

    def unlock_master_key(self, password: str) -> bytes | None:
        if self._verify_password(password):
            with open(os.path.join(self.path, "password", "master_key.txt"), "rb") as f:
                data = f.read()
                salt = data[:16]

            return self._generate_master_key(password, salt)
        else:
            messagebox.showerror(self.name, "Incorrect password please try again")
            return None

    def encrypt_content(self, content: bytes, master_key: bytes) -> bytes:
        cipher_suite = Fernet(master_key)
        return cipher_suite.encrypt(content)

    def decrypt_content(self, content: bytes, master_key: bytes) -> bytes:
        cipher_suite = Fernet(master_key)
        return cipher_suite.decrypt(content)
