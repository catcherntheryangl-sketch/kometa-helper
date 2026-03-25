import customtkinter as ctk
from src.utils.constants import COLORS

class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Center content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            self, 
            text="Welcome to Kometa Helper", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["text_primary"]
        ).grid(row=0, column=0, pady=(100, 20))

        ctk.CTkLabel(
            self,
            text="Use the sidebar to install dependencies or manage your Kometa instance.",
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text_secondary"]
        ).grid(row=1, column=0, sticky="n")
