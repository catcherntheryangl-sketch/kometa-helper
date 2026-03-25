import customtkinter as ctk
from src.utils.constants import COLORS

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        ctk.CTkLabel(
            self, 
            text="Settings", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["text_primary"]
        ).pack(anchor="w", padx=30, pady=30)

        # Theme Selection
        theme_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"])
        theme_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(theme_frame, text="Appearance Mode").pack(side="left", padx=20, pady=20)
        
        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode
        )
        self.theme_menu.pack(side="right", padx=20, pady=20)

    def change_appearance_mode(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)
