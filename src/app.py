"""
KometaHelperApp - Main application orchestrator
"""

import customtkinter as ctk
from src.ui.main_window import MainWindow
from src.core.config_manager import ConfigManager
from src.core.kometa_manager import KometaManager


class KometaHelperApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.config_manager = ConfigManager()
        self.kometa_manager = KometaManager(self.config_manager)

        self.root = ctk.CTk()
        self.root.title("Kometa Helper")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        # Set window icon if available
        try:
            self.root.iconbitmap("assets/icon.ico")
        except Exception:
            pass

        self.main_window = MainWindow(
            self.root,
            config_manager=self.config_manager,
            kometa_manager=self.kometa_manager,
        )

    def run(self):
        self.root.mainloop()
