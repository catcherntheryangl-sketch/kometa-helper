"""
MainWindow - Root window with sidebar navigation and page frame switching
"""

import customtkinter as ctk
from src.ui.theme import COLORS, FONTS, NAV_ITEMS
from src.ui.pages.dashboard import DashboardPage
from src.ui.pages.install import InstallPage
from src.ui.pages.connections import ConnectionsPage
from src.ui.pages.yaml_editor import YamlEditorPage
from src.ui.pages.collections import CollectionsPage
from src.ui.pages.runner import RunnerPage
from src.ui.pages.scheduler import SchedulerPage
from src.ui.pages.logs import LogsPage
from src.ui.pages.backups import BackupsPage
from src.ui.pages.settings import SettingsPage


class MainWindow:
    def __init__(self, root: ctk.CTk, config_manager, kometa_manager):
        self.root = root
        self.config = config_manager
        self.kometa = kometa_manager

        self._current_page = None
        self._nav_buttons = {}
        self._pages = {}

        self._build_layout()
        self._build_sidebar()
        self._build_content_area()
        self._init_pages()

        # Navigate to dashboard on start
        self.navigate("dashboard")

        # Status updates from kometa manager
        self.kometa.on_status_change = self._on_kometa_status_change

    def _build_layout(self):
        self.root.configure(fg_color=COLORS["bg_dark"])
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=220,
            corner_radius=0,
            fg_color=COLORS["bg_panel"],
            border_width=0,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(len(NAV_ITEMS) + 2, weight=1)

        # Logo area
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=70)
        logo_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        logo_frame.grid_propagate(False)

        ctk.CTkLabel(
            logo_frame,
            text="⚡ Kometa",
            font=ctk.CTkFont("Segoe UI Semibold", 20),
            text_color=COLORS["accent"],
        ).place(relx=0.5, rely=0.45, anchor="center")
        ctk.CTkLabel(
            logo_frame,
            text="Helper",
            font=ctk.CTkFont("Segoe UI Light", 13),
            text_color=COLORS["text_secondary"],
        ).place(relx=0.5, rely=0.72, anchor="center")

        # Divider
        ctk.CTkFrame(
            self.sidebar, height=1, fg_color=COLORS["border"]
        ).grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))

        # Nav buttons
        for i, (icon, label, page_key) in enumerate(NAV_ITEMS):
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {icon}  {label}",
                anchor="w",
                font=ctk.CTkFont("Segoe UI", 12),
                fg_color="transparent",
                text_color=COLORS["text_secondary"],
                hover_color=COLORS["nav_hover_bg"],
                corner_radius=8,
                height=40,
                command=lambda k=page_key: self.navigate(k),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=12, pady=2)
            self._nav_buttons[page_key] = btn

        # Status indicator at bottom of sidebar
        self._status_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self._status_frame.grid(row=len(NAV_ITEMS) + 3, column=0, sticky="ew", padx=12, pady=12)

        self._status_dot = ctk.CTkLabel(
            self._status_frame,
            text="●",
            font=ctk.CTkFont("Segoe UI", 14),
            text_color=COLORS["status_idle"],
        )
        self._status_dot.grid(row=0, column=0, padx=(0, 6))

        self._status_label = ctk.CTkLabel(
            self._status_frame,
            text="Kometa: Idle",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_secondary"],
        )
        self._status_label.grid(row=0, column=1, sticky="w")

    def _build_content_area(self):
        self.content_frame = ctk.CTkFrame(
            self.root,
            corner_radius=0,
            fg_color=COLORS["bg_dark"],
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def _init_pages(self):
        page_classes = {
            "dashboard":   DashboardPage,
            "install":     InstallPage,
            "connections": ConnectionsPage,
            "yaml_editor": YamlEditorPage,
            "collections": CollectionsPage,
            "runner":      RunnerPage,
            "scheduler":   SchedulerPage,
            "logs":        LogsPage,
            "backups":     BackupsPage,
            "settings":    SettingsPage,
        }
        for key, cls in page_classes.items():
            page = cls(
                self.content_frame,
                config_manager=self.config,
                kometa_manager=self.kometa,
                navigate=self.navigate,
            )
            page.grid(row=0, column=0, sticky="nsew")
            self._pages[key] = page

    def navigate(self, page_key: str):
        if self._current_page == page_key:
            return

        # Hide all pages
        for page in self._pages.values():
            page.grid_remove()

        # Show target page
        if page_key in self._pages:
            self._pages[page_key].grid()
            if hasattr(self._pages[page_key], "on_show"):
                self._pages[page_key].on_show()

        # Update nav button styles
        for key, btn in self._nav_buttons.items():
            if key == page_key:
                btn.configure(
                    fg_color=COLORS["nav_active_bg"],
                    text_color=COLORS["accent"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_secondary"],
                )

        self._current_page = page_key

    def _on_kometa_status_change(self, status: str):
        color_map = {
            "running": COLORS["status_running"],
            "stopped": COLORS["status_stopped"],
            "idle":    COLORS["status_idle"],
        }
        label_map = {
            "running": "Kometa: Running",
            "stopped": "Kometa: Stopped",
            "idle":    "Kometa: Idle",
        }
        color = color_map.get(status, COLORS["status_idle"])
        label = label_map.get(status, f"Kometa: {status.capitalize()}")
        self.root.after(0, lambda: (
            self._status_dot.configure(text_color=color),
            self._status_label.configure(text=label),
        ))
