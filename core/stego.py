"""
LSB steganography for CipherPixel
Hide bytes inside least significant bits of RGB pixels
"""
from PIL import Image

def hide_bytes_in_image(cover_image_path: str, output_path: str, data: bytes):
    img = Image.open(cover_image_path)
    img = img.convert("RGB")
    pixels = list(img.getdata())
    data_bits = ''.join(f"{byte:08b}" for byte in data)
    data_len = len(data_bits)
    length_bits = f"{data_len:032b}"
    all_bits = length_bits + data_bits
    capacity = len(pixels)*3
    if len(all_bits) > capacity:
        raise ValueError(f"Data too large for image capacity {capacity} bits")
    new_pixels=[]
    bit_idx=0
    for r,g,b in pixels:
        nr = (r & ~1)
        ng = (g & ~1)
        nb = (b & ~1)
        if bit_idx < len(all_bits):
            nr |= int(all_bits[bit_idx]); bit_idx+=1
        if bit_idx < len(all_bits):
            ng |= int(all_bits[bit_idx]); bit_idx+=1
        if bit_idx < len(all_bits):
            nb |= int(all_bits[bit_idx]); bit_idx+=1
        new_pixels.append((nr,ng,nb))
    img.putdata(new_pixels)
    img.save(output_path)

def extract_bytes_from_image(stego_image_path: str) -> bytes:
    img = Image.open(stego_image_path)
    img = img.convert("RGB")
    pixels = list(img.getdata())
    bits=''
    # read first 32 bits
    for i in range(0, (32+2)//3 + 2):
        r,g,b = pixels[i]
        bits += str(r&1) + str(g&1) + str(b&1)
        if len(bits) >= 32:
            break
    data_len = int(bits[:32],2)
    # extract next data_len bits
    all_bits=''
    bit_count=0
    for r,g,b in pixels:
        for ch in (r,g,b):
            if bit_count >= 32 + data_len:
                break
            all_bits += str(ch & 1)
            bit_count += 1
        if bit_count >= 32 + data_len:
            break
    data_bits = all_bits[32:32+data_len]
    data_bytes = bytearray()
    for i in range(0,len(data_bits),8):
        byte = data_bits[i:i+8]
        if len(byte) < 8:
            break
        data_bytes.append(int(byte,2))
    return bytes(data_bytes)

if __name__ == "__main__":
    from PIL import Image
    im = Image.new("RGB",(100,100),(120,130,140))
    im.save("temp_cover.png")
    hide_bytes_in_image("temp_cover.png","temp_stego.png",b"hello world")
    print(extract_bytes_from_image("temp_stego.png"))
