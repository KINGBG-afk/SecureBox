from cryptography.fernet import Fernet
import json


class Cryptor:
    def __init__(self, path: str) -> None:
        self.path = path

    # key
    def _encrypt_key(self, key: bytes) -> list:
        key = str(key)[2:-1]
        enkey = []
        for char in key:
            enkey.append(ord(char) + 1)

        return enkey

    def _decrypt_key(self, file_name: str) -> bytes:
        with open(self.path + rf"\keys\{file_name}.key", "r") as key_file:
            crypt_key = json.loads(key_file.read())

        return bytes("".join(chr(num - 1) for num in crypt_key), "utf-8")

    def _generate_key(self, file_name: str) -> bytes:
        key = Fernet.generate_key()
        with open(self.path + rf"\keys\{file_name}.key", "w") as key_file:
            dkey = self._encrypt_key(key)
            key_file.write(str(dkey))

        return key

    def encrypt_content(self, content: bytes, file_name: str) -> bytes:
        cipher_suite = Fernet(self._generate_key(file_name))
        return cipher_suite.encrypt(content)

    def decrypt_content(self, content: bytes, file_name: str) -> bytes:
        cipher_suite = Fernet(self._decrypt_key(file_name))
        return cipher_suite.decrypt(content)


if __name__ == "__main__":
    # cypting and decrypting wroks
    path = r"D:\programming\Python\GUI\SecureBox"
    c = Cryptor(path)
    with open(path + r"\test\test.txt", "rb") as f:
        content = f.read()

    data = c.encrypt_content(content, "test")

    with open(path + r"\test\test.txt", "wb") as f:
        f.write(data)

    # decrypt file
    with open(path + r"\test\test.txt", "rb") as f:
        content = f.read()

    ddata = c.decrypt_content(content, "test")
    with open(path + r"\test\test.txt", "wb") as f:
        f.write(ddata)
