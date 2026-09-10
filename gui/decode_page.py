"""
Decode page UI for CipherPixel
- Select stego image or packet JSON
- Choose recipient private key (to decrypt AES key)
- Choose sender public key (to verify signature)
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os, json

from core.stego import extract_bytes_from_image
from core.aes_crypto import aes_decrypt_bytes
from core.rsa_tools import verify_signature_bytes, rsa_decrypt_bytes
from core.hasher import sha256_digest_bytes
from core.packet import parse_packet
from utils.file_ops import read_packet_file
from utils.keys import load_rsa_private_key, load_rsa_public_key

BTN_WIDTH = 260
BTN_HEIGHT = 40

class DecodePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.stego_path = None
        self.packet_path = None
        self.recipient_priv = None
        self.sender_pub = None

        # Title
        ctk.CTkLabel(
            self,
            text="🔓 CipherPixel — Decode Message",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 15))

        # Input Selection
        ctk.CTkLabel(
            self,
            text="Select Input Source",
            font=("Arial", 14, "bold")
        ).pack(pady=(6, 6))

        ctk.CTkButton(
            self,
            text="Select Stego Image",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            command=self.select_image
        ).pack(pady=6)

        ctk.CTkButton(
            self,
            text="Select Packet JSON (Optional)",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            command=self.select_packet
        ).pack(pady=6)

        # Key Selection
        ctk.CTkLabel(
            self,
            text="Key Selection",
            font=("Arial", 14, "bold")
        ).pack(pady=(18, 6))

        ctk.CTkButton(
            self,
            text="Select Your Private Key (Decrypt)",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            command=self.select_recipient_priv
        ).pack(pady=6)

        ctk.CTkButton(
            self,
            text="Select Sender Public Key (Verify)",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            command=self.select_sender_pub
        ).pack(pady=6)

        # Decode Action
        self.decode_btn = ctk.CTkButton(
            self,
            text="Decode & Verify Message",
            width=BTN_WIDTH + 40,
            height=46,
            fg_color="#1f6aa5",
            hover_color="#155a8a",
            font=("Arial", 14, "bold"),
            command=self.decode_message
        )
        self.decode_btn.pack(pady=(22, 16))

        # Output
        ctk.CTkLabel(
            self,
            text="Decoded Message Output",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 4))

        self.textbox = ctk.CTkTextbox(
            self,
            width=720,
            height=200,
            corner_radius=10
        )
        self.textbox.pack(pady=(4, 18))

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.stego_path = path
            messagebox.showinfo("Stego Image Selected", os.path.basename(path))

    def select_packet(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.packet_path = path
            messagebox.showinfo("Packet Selected", os.path.basename(path))

    def select_recipient_priv(self):
        path = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        if path:
            self.recipient_priv = path
            messagebox.showinfo("Private Key Selected", os.path.basename(path))

    def select_sender_pub(self):
        path = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        if path:
            self.sender_pub = path
            messagebox.showinfo("Public Key Selected", os.path.basename(path))

    def decode_message(self):
        if not self.recipient_priv:
            messagebox.showerror("Missing Input", "Please select your private key.")
            return
        if not self.sender_pub:
            messagebox.showerror("Missing Input", "Please select sender public key.")
            return

        try:
            priv = load_rsa_private_key(self.recipient_priv)
            sender_pub = load_rsa_public_key(self.sender_pub)
        except Exception as e:
            messagebox.showerror("Key Error", str(e))
            return

        if self.packet_path:
            try:
                packet = read_packet_file(self.packet_path)
            except Exception as e:
                messagebox.showerror("Packet Error", str(e))
                return
        elif self.stego_path:
            try:
                extracted = extract_bytes_from_image(self.stego_path)
                packet = json.loads(extracted.decode("utf-8"))
            except Exception as e:
                messagebox.showerror("Extraction Error", str(e))
                return
        else:
            messagebox.showerror("Missing Input", "Please select a stego image or packet file.")
            return

        parsed = parse_packet(packet)

        try:
            aes_key = rsa_decrypt_bytes(parsed["enc_aes_key"], priv)
            plaintext = aes_decrypt_bytes(parsed["iv"], parsed["ciphertext"], aes_key)
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))
            return

        try:
            valid_sig = verify_signature_bytes(parsed["hash"], parsed["signature"], sender_pub)
        except Exception:
            valid_sig = False

        actual_hash = sha256_digest_bytes(plaintext)
        hash_ok = actual_hash == parsed["hash"]

        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", plaintext.decode("utf-8", errors="replace"))

        status = (
            f"\n\nSignature Verification: {'VALID' if valid_sig else 'INVALID'}"
            f"\nMessage Integrity: {'OK' if hash_ok else 'FAILED'}"
        )
        self.textbox.insert("end", status)

        if valid_sig and hash_ok:
            messagebox.showinfo("Success", "Message decoded and verified successfully!")
        else:
            messagebox.showwarning(
                "Verification Warning",
                "Signature or integrity check failed.\nMessage may be altered."
            )
