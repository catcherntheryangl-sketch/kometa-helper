import customtkinter as ctk
from src.ui.pages.home import HomePage
from src.ui.pages.install import InstallPage
from src.ui.pages.settings import SettingsPage
from src.utils.constants import COLORS

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kometa Helper")
        self.geometry("1000x650")
        self.configure(fg_color=COLORS["bg_primary"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._init_sidebar()
        self._init_pages()
        self.show_page("home")

    def _init_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color=COLORS["bg_secondary"], corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="KOMETA", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        self.nav_buttons = {}
        for page in [("Home", "home"), ("Install", "install"), ("Settings", "settings")]:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=page[0], 
                command=lambda p=page[1]: self.show_page(p),
                fg_color="transparent",
                text_color=COLORS["text_primary"],
                hover_color=COLORS["bg_hover"]
            )
            btn.pack(pady=5, padx=10, fill="x")
            self.nav_buttons[page[1]] = btn

    def _init_pages(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.pages = {
            "home": HomePage(self.container),
            "install": InstallPage(self.container),
            "settings": SettingsPage(self.container)
        }

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name):
        for name, page in self.pages.items():
            if name == page_name:
                page.grid(row=0, column=0, sticky="nsew")
                self.nav_buttons[name].configure(fg_color=COLORS["bg_hover"])
            else:
                page.grid_forget()
                self.nav_buttons[name].configure(fg_color="transparent")
