"""
Encode page UI for CipherPixel
- Select cover image
- Enter secret message
- Choose sender private key (for signing)
- Choose recipient public key (for encrypting AES key)
- Encode + save stego image and packet
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os, json

from core.stego import hide_bytes_in_image
from core.aes_crypto import generate_aes_key, aes_encrypt_bytes
from core.rsa_tools import sign_bytes, rsa_encrypt_bytes
from core.hasher import sha256_digest_bytes
from core.packet import build_packet
from utils.file_ops import write_packet_file
from utils.keys import load_rsa_private_key, load_rsa_public_key
from PIL import Image

AES_KEY_SIZE = 16  # AES-128

BTN_WIDTH = 260
BTN_HEIGHT = 40

class EncodePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.cover_path = None
        self.sender_priv_path = None
        self.recipient_pub_path = None

        # Title
        ctk.CTkLabel(
            self,
            text="🔐 CipherPixel — Encode Message",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 15))

        # Cover Image Selection
        self.select_cover_btn = ctk.CTkButton(
            self,
            text="Select Cover Image",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            command=self.select_image
        )
        self.select_cover_btn.pack(pady=6)

        # Message Input
        ctk.CTkLabel(
            self,
            text="Secret Message to Hide",
            font=("Arial", 14, "bold")
        ).pack(pady=(14, 4))

        self.message_entry = ctk.CTkTextbox(
            self,
            width=650,
            height=140,
            corner_radius=10
        )
        self.message_entry.pack(pady=6)

        # Key Selection Section
        ctk.CTkLabel(
            self,
            text="Key Selection",
            font=("Arial", 14, "bold")
        ).pack(pady=(18, 6))

        self.select_sender_priv_btn = ctk.CTkButton(
            self,
            text="Select Your Private Key (Signing)",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            command=self.select_sender_priv
        )
        self.select_sender_priv_btn.pack(pady=6)

        self.select_recipient_pub_btn = ctk.CTkButton(
            self,
            text="Select Recipient Public Key (Encryption)",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            command=self.select_recipient_pub
        )
        self.select_recipient_pub_btn.pack(pady=6)

        # Encode Button
        self.encode_btn = ctk.CTkButton(
            self,
            text="Encode & Save Secure Image",
            width=BTN_WIDTH + 40,
            height=46,
            fg_color="#1f6aa5",
            hover_color="#155a8a",
            font=("Arial", 14, "bold"),
            command=self.encode_message
        )
        self.encode_btn.pack(pady=(22, 18))

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.cover_path = path
            messagebox.showinfo("Cover Image Selected", os.path.basename(path))

    def select_sender_priv(self):
        path = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        if path:
            self.sender_priv_path = path
            messagebox.showinfo("Private Key Selected", os.path.basename(path))

    def select_recipient_pub(self):
        path = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        if path:
            self.recipient_pub_path = path
            messagebox.showinfo("Public Key Selected", os.path.basename(path))

    def _estimate_capacity_bits(self, image_path: str) -> int:
        img = Image.open(image_path).convert("RGB")
        pixels = img.size[0] * img.size[1]
        return pixels * 3

    def encode_message(self):
        if not self.cover_path:
            messagebox.showerror("Missing Input", "Please select a cover image.")
            return
        if not self.sender_priv_path:
            messagebox.showerror("Missing Input", "Please select your private key.")
            return
        if not self.recipient_pub_path:
            messagebox.showerror("Missing Input", "Please select recipient public key.")
            return

        message = self.message_entry.get("1.0", "end").strip()
        if not message:
            messagebox.showerror("Missing Input", "Please enter a secret message.")
            return

        try:
            priv_key = load_rsa_private_key(self.sender_priv_path)
            recipient_pub = load_rsa_public_key(self.recipient_pub_path)
        except Exception as e:
            messagebox.showerror("Key Error", str(e))
            return

        msg_bytes = message.encode("utf-8")
        msg_hash = sha256_digest_bytes(msg_bytes)

        try:
            signature = sign_bytes(msg_hash, priv_key)
        except Exception as e:
            messagebox.showerror("Signing Failed", str(e))
            return

        aes_key = generate_aes_key() if generate_aes_key.__code__.co_argcount == 0 else generate_aes_key(AES_KEY_SIZE)

        try:
            iv, ciphertext = aes_encrypt_bytes(msg_bytes, aes_key)
            enc_aes_key = rsa_encrypt_bytes(aes_key, recipient_pub)
        except Exception as e:
            messagebox.showerror("Encryption Failed", str(e))
            return

        packet = build_packet(
            ciphertext, iv, enc_aes_key, signature, msg_hash,
            {"original_filename": os.path.basename(self.cover_path)}
        )

        packet_bytes = json.dumps(packet).encode("utf-8")

        try:
            capacity_bits = self._estimate_capacity_bits(self.cover_path)
            needed_bits = len(packet_bytes) * 8 + 32
            if needed_bits > capacity_bits:
                messagebox.showerror(
                    "Embedding Error",
                    "Selected image is too small for this message.\nPlease choose a larger image."
                )
                return
        except Exception:
            pass

        packet_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if not packet_path:
            return

        write_packet_file(packet, packet_path)

        stego_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if not stego_path:
            return

        try:
            hide_bytes_in_image(self.cover_path, stego_path, packet_bytes)
        except Exception as e:
            messagebox.showerror("Embedding Failed", str(e))
            return

        messagebox.showinfo(
            "Success",
            "Message encoded successfully!\n\n"
            f"Stego Image:\n{stego_path}\n\nPacket File:\n{packet_path}"
        )
