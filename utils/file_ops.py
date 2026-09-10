"""
Basic file operations for CipherPixel.
Handles:
- Loading images
- Saving images
- Reading JSON packets
- Writing JSON packets
"""

import json
from pathlib import Path
from PIL import Image

def save_image(pil_image: Image.Image, path: str):
    """Save a PIL Image to disk."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    pil_image.save(str(p))

def load_image(path: str) -> Image.Image:
    """Load an image using Pillow."""
    return Image.open(path)

def write_packet_file(packet: dict, path: str):
    """Save packet (dict) as JSON."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(packet, f, indent=2)

def read_packet_file(path: str) -> dict:
    """Load packet from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    demo = {"msg": "hello", "val": 123}
    write_packet_file(demo, "data/encoded_packets/demo.json")
    print(read_packet_file("data/encoded_packets/demo.json"))
