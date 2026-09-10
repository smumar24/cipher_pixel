"""
RSA key generation + loading and saving helpers.
Beginner-friendly and used throughout CipherPixel.
"""

from Crypto.PublicKey import RSA

def generate_rsa_keypair(bits: int = 2048) -> RSA.RsaKey:
    """Generate a fresh RSA private key."""
    return RSA.generate(bits)

def save_rsa_private_key(private_key: RSA.RsaKey, path: str, passphrase: str = None):
    """Save RSA private key to file (PEM format)."""
    pem = private_key.export_key(
        format='PEM',
        passphrase=passphrase,
        pkcs=8
    ) if passphrase else private_key.export_key()

    with open(path, "wb") as f:
        f.write(pem)

def save_rsa_public_key(public_key: RSA.RsaKey, path: str):
    """Save RSA public key to file."""
    with open(path, "wb") as f:
        f.write(public_key.export_key())

def load_rsa_private_key(path: str, passphrase: str = None) -> RSA.RsaKey:
    """Load RSA private key."""
    with open(path, "rb") as f:
        data = f.read()
    return RSA.import_key(data, passphrase=passphrase)

def load_rsa_public_key(path: str) -> RSA.RsaKey:
    """Load RSA public key."""
    with open(path, "rb") as f:
        data = f.read()
    return RSA.import_key(data)

def generate_and_save_rsa_keys(private_path: str, public_path: str, bits: int = 2048):
    """Convenience function to generate and save both keys."""
    key = generate_rsa_keypair(bits)
    save_rsa_private_key(key, private_path)
    save_rsa_public_key(key.publickey(), public_path)

if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    generate_and_save_rsa_keys("data/private.pem", "data/public.pem")
    print("Generated RSA keys in data/ folder.")
