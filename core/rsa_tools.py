"""
RSA signing, verification, encryption, and decryption (raw-bytes helpers)
Uses PyCryptodome RSA module
"""
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

def sign_bytes(data: bytes, private_key: RSA.RsaKey) -> bytes:
    """Return raw signature bytes (not base64). Signing is over provided data (usually the hash)."""
    h = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

def verify_signature_bytes(data: bytes, signature: bytes, public_key: RSA.RsaKey) -> bool:
    """Verify signature bytes; returns True/False."""
    h = SHA256.new(data)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

def rsa_encrypt_bytes(data: bytes, public_key: RSA.RsaKey) -> bytes:
    """Encrypt data with RSA public key (OAEP). Returns bytes."""
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)

def rsa_decrypt_bytes(ciphertext: bytes, private_key: RSA.RsaKey) -> bytes:
    """Decrypt RSA ciphertext with private key (OAEP)."""
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext)

def to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode()

def from_b64(s: str) -> bytes:
    return base64.b64decode(s)

if __name__ == "__main__":
    from utils.keys import generate_rsa_keypair
    key = generate_rsa_keypair()
    pub = key.publickey()
    msg = b"CipherPixel RSA test"
    sig = sign_bytes(msg, key)
    print("Signature len:", len(sig))
    print("Verify:", verify_signature_bytes(msg, sig, pub))
    enc = rsa_encrypt_bytes(b"secret", pub)
    dec = rsa_decrypt_bytes(enc, key)
    print("dec:", dec)
