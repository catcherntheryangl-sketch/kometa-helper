import customtkinter as ctk
import webbrowser
from src.utils.constants import COLORS

class InstallPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.columnconfigure(0, weight=1)
        self._build()

    def _build(self):
        """Build the installation progress UI."""
        # Main Title
        ctk.CTkLabel(
            self, 
            text="Installation Setup", 
            font=ctk.CTkFont("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"]
        ).grid(row=0, column=0, sticky="w", padx=30, pady=(30, 10))

        # Description
        ctk.CTkLabel(
            self,
            text="Follow the steps below to set up Kometa on your system.",
            font=ctk.CTkFont("Segoe UI", 14),
            text_color=COLORS["text_secondary"]
        ).grid(row=1, column=0, sticky="w", padx=30, pady=(0, 20))

        # Scrollable container for steps
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        scroll.columnconfigure(0, weight=1)

        # Step 1: Python
        self._build_python_step(scroll, row=0)
        
        # Step 2: Git
        self._build_git_step(scroll, row=1)

    def make_card(self, parent):
        return ctk.CTkFrame(parent, fg_color=COLORS["bg_secondary"], corner_radius=12)

    def make_button(self, parent, text, command, style="primary", width=100):
        fg = COLORS["accent"] if style == "primary" else COLORS["bg_hover"]
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=fg,
            hover_color=COLORS["accent"],
            corner_radius=8,
            width=width,
            height=36
        )

    def _build_python_step(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 8))
        
        ctk.CTkLabel(
            header, 
            text="Step 1 — Python", 
            font=ctk.CTkFont("Segoe UI Semibold", 14),
            text_color=COLORS["text_primary"]
        ).pack(side="left")

        # Fixed text_color
        self._python_badge = ctk.CTkLabel(
            header,
            text=" Checking... ",
            font=ctk.CTkFont("Segoe UI Semibold", 10),
            text_color="#d29922", 
            fg_color=COLORS["accent_yellow"] + "22",
            corner_radius=4,
        )
        self._python_badge.pack(side="right")

        self._python_detail = ctk.CTkLabel(
            card,
            text="Kometa requires Python 3.10 or newer.",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"]
        )
        self._python_detail.pack(anchor="w", padx=20, pady=(0, 4))

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(anchor="w", padx=20, pady=(0, 16))

        self.make_button(btn_row, "Check Python", self._check_python, "secondary", width=140).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            btn_row,
            text="Download Python 3.12",
            command=self._open_python_download,
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color="transparent",
            text_color=COLORS["accent"],
            hover_color=COLORS["bg_hover"],
            corner_radius=8,
            width=160,
            height=36
        ).pack(side="left")

    def _build_git_step(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 8))
        
        ctk.CTkLabel(
            header, 
            text="Step 2 — Git", 
            font=ctk.CTkFont("Segoe UI Semibold", 14),
            text_color=COLORS["text_primary"]
        ).pack(side="left")

        self._git_badge = ctk.CTkLabel(
            header,
            text=" Checking... ",
            font=ctk.CTkFont("Segoe UI Semibold", 10),
            text_color=COLORS["accent_yellow"],
            fg_color=COLORS["accent_yellow"] + "22",
            corner_radius=4,
        )
        self._git_badge.pack(side="right")

    def _check_python(self):
        pass

    def _open_python_download(self):
        webbrowser.open("https://www.python.org/downloads/")
