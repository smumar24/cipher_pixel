# CipherPixel (Educational Steganography + Cryptography Project)

CipherPixel is a secure image-based data hiding system that uses:
- AES encryption
- RSA digital signatures
- SHA-256 hashing
- LSB steganography
- CustomTkinter GUI

This is a 3rd-semester level Information Security project designed to teach
cryptography + steganography concepts in a simple and beginner-friendly way.

## Installation
1. Create a virtual environment (recommended):
   python -m venv venv
   venv\Scripts\activate   # windows
   source venv/bin/activate  # linux/mac

2. Install libraries:
   pip install -r requirements.txt

## Project Structure
- core/ → cryptography, hashing, steganography, packet builder
- gui/  → CustomTkinter interface (encode/decode)
- utils/ → file operations + RSA key helpers
- data/ → RSA keys, packet files, output images

## Quick Start
Generate RSA keys:
python -c "from utils.keys import generate_and_save_rsa_keys; generate_and_save_rsa_keys('data/private.pem','data/public.pem')"
