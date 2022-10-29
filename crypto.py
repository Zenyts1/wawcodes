import time
import base64

time.clock = time.perf_counter_ns

from Crypto import Random
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class Crypto:
    def __init__(self, key):
        self.key = key
        self.cipher = AES.new(sha256(self.key).digest(), AES.MODE_ECB)

    def encrypt(self, text):
        iv = Random.get_random_bytes(16)
        return base64.b64encode(
            iv[:8] + self.cipher.encrypt(pad(text, 16), iv) + iv[8:]
        )

    def decrypt(self, text):
        text = base64.b64decode(text)
        return unpad(self.cipher.decrypt(text[8:-8], text[:8] + text[-8:]), 16)


if __name__ == "__main__":
    key = Random.get_random_bytes(32)
    print(key)
    print(sha256(key).digest())
    cipher = Crypto(key)
    print(cipher.encrypt(b"yey !"))
