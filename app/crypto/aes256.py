import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher:

    def __init__(self, key: bytes):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode()

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


import pyaes

# 16 byte block of plain text
plaintext = "Hello World!!!!!"
plaintext_bytes = [ ord(c) for c in plaintext ]

# 32 byte key (256 bit)
key = "This_key_for_demo_purposes_only!"

# Our AES instance
aes = pyaes.AES(key)

# Encrypt!
ciphertext = aes.encrypt(plaintext_bytes)

# [55, 250, 182, 25, 185, 208, 186, 95, 206, 115, 50, 115, 108, 58, 174, 115]
print repr(ciphertext)

# Decrypt!
decrypted = aes.decrypt(ciphertext)

# True
print decrypted == plaintext_bytes
