"""
Hasher module for CipherPixel
Uses SHA-256 hashing for data integrity checks
"""
import hashlib

def sha256_digest_bytes(data: bytes) -> bytes:
    """Return SHA-256 digest as bytes."""
    return hashlib.sha256(data).digest()

def sha256_digest_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

if __name__ == "__main__":
    print(sha256_digest_hex(b"hello"))
