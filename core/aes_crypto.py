"""
AES encryption and decryption module for CipherPixel
Uses AES-CBC mode with PKCS7 padding.
Provides helpers that operate on raw bytes.
"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

BLOCK_SIZE = 16  # AES block size in bytes

def generate_aes_key(length=16):
    """Generate a random AES key (16/24/32 bytes)."""
    return get_random_bytes(length)

def aes_encrypt_bytes(plaintext: bytes, key: bytes):
    """
    Encrypt bytes using AES-CBC and return tuple (iv, ciphertext) as bytes.
    """
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, BLOCK_SIZE))
    return iv, ciphertext

def aes_decrypt_bytes(iv: bytes, ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt AES-CBC ciphertext and return plaintext bytes."""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
    return plaintext

def to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode()

def from_b64(s: str) -> bytes:
    return base64.b64decode(s)

if __name__ == "__main__":
    key = generate_aes_key(16)
    msg = b"Hello AES in CipherPixel"
    iv, ct = aes_encrypt_bytes(msg, key)
    print("iv b64:", to_b64(iv))
    print("ct b64:", to_b64(ct))
    pt = aes_decrypt_bytes(iv, ct, key)
    print("Decrypted:", pt)
