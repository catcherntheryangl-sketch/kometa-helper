import customtkinter as ctk
from src.ui.main_window import MainWindow
from src.utils.constants import APP_CONFIG

class KometaHelperApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = MainWindow()

    def run(self):
        self.root.mainloop()
        return 0
