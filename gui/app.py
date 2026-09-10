"""
Main application window for CipherPixel
- Handles navigation between Encode and Decode pages
- Uses CustomTkinter for modern look
"""

import customtkinter as ctk
import os

from gui.encode_page import EncodePage
from gui.decode_page import DecodePage

ctk.set_appearance_mode("Dark")  # "Dark" or "Light"
ctk.set_default_color_theme("blue")

NAV_BTN_WIDTH = 160
NAV_BTN_HEIGHT = 42

class CipherPixelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CipherPixel")
        self.geometry("980x640")
        self.resizable(False, False)

        # ===== App Icon (Portable & Safe) =====
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ICON_PATH = os.path.join(BASE_DIR, "..", "assets", "app_icon.ico")

        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)
        # =====================================

        # Sidebar / Navigation Frame
        self.nav_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.nav_frame.pack(side="left", fill="y")

        # App Title
        ctk.CTkLabel(
            self.nav_frame,
            text="CipherPixel",
            font=("Arial", 22, "bold")
        ).pack(pady=(30, 6))

        ctk.CTkLabel(
            self.nav_frame,
            text="Secure Image Messaging",
            font=("Arial", 12)
        ).pack(pady=(0, 30))

        # Navigation Buttons
        self.encode_btn = ctk.CTkButton(
            self.nav_frame,
            text="🔐 Encode",
            width=NAV_BTN_WIDTH,
            height=NAV_BTN_HEIGHT,
            command=lambda: self.show_frame("EncodePage")
        )
        self.encode_btn.pack(pady=10, padx=20)

        self.decode_btn = ctk.CTkButton(
            self.nav_frame,
            text="🔓 Decode",
            width=NAV_BTN_WIDTH,
            height=NAV_BTN_HEIGHT,
            command=lambda: self.show_frame("DecodePage")
        )
        self.decode_btn.pack(pady=10, padx=20)

        # Main Container
        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(side="right", fill="both", expand=True)

        self.frames = {}
        for F in (EncodePage, DecodePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("EncodePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = CipherPixelApp()
    app.mainloop()
