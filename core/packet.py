"""
Packet builder for CipherPixel
- Combines AES ciphertext, RSA-encrypted AES key, RSA signature (over hash), and hash into a JSON-ready dict
- All binary fields are base64-encoded for safe JSON storage
"""
import base64
from typing import Dict

def build_packet(ciphertext: bytes, iv: bytes, rsa_encrypted_key: bytes, signature: bytes, hash_bytes: bytes, extra_info: Dict = None) -> Dict:
    packet = {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "iv": base64.b64encode(iv).decode(),
        "enc_aes_key": base64.b64encode(rsa_encrypted_key).decode(),
        "signature": base64.b64encode(signature).decode(),
        "hash": base64.b64encode(hash_bytes).decode()
    }
    if extra_info:
        packet.update(extra_info)
    return packet

def parse_packet(packet: Dict) -> Dict:
    return {
        "ciphertext": base64.b64decode(packet["ciphertext"]),
        "iv": base64.b64decode(packet["iv"]),
        "enc_aes_key": base64.b64decode(packet["enc_aes_key"]),
        "signature": base64.b64decode(packet["signature"]),
        "hash": base64.b64decode(packet["hash"]),
        "extra_info": {k:v for k,v in packet.items() if k not in ("ciphertext","iv","enc_aes_key","signature","hash")}
    }

if __name__ == "__main__":
    pkt = build_packet(b"ct", b"iviv", b"rak", b"sig", b"hsh", {"fname":"demo"})
    print(pkt)
    print(parse_packet(pkt))
