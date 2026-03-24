"""
DashboardPage - Status overview, quick actions, run history
"""

import customtkinter as ctk
from src.ui.pages.base_page import BasePage
from src.ui.theme import COLORS


class DashboardPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=32, pady=24)
        scroll.grid_columnconfigure((0, 1), weight=1)

        # Header
        header = self.make_page_header(scroll, "Dashboard", "Welcome to Kometa Helper")
        header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 24))

        # Status cards row
        self._build_status_cards(scroll)

        # Quick actions
        self._build_quick_actions(scroll)

        # Kometa info card
        self._build_info_card(scroll)

    def _build_status_cards(self, parent):
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        status_data = [
            ("Kometa Status", "Not Installed", COLORS["accent_red"], "status"),
            ("Last Run", "Never", COLORS["text_secondary"], "last_run"),
            ("Config", "Not Set", COLORS["accent_yellow"], "config"),
            ("Libraries", "0", COLORS["text_secondary"], "libraries"),
        ]

        self._status_labels = {}
        for i, (title, default, color, key) in enumerate(status_data):
            card = self.make_card(cards_frame)
            card.grid(row=0, column=i, sticky="ew", padx=(0, 12) if i < 3 else 0)

            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont("Segoe UI", 11),
                text_color=COLORS["text_secondary"],
            ).pack(anchor="w", padx=16, pady=(14, 2))

            val_label = ctk.CTkLabel(
                card,
                text=default,
                font=ctk.CTkFont("Segoe UI Semibold", 18),
                text_color=color,
            )
            val_label.pack(anchor="w", padx=16, pady=(0, 14))
            self._status_labels[key] = val_label

    def _build_quick_actions(self, parent):
        section = self.make_card(parent)
        section.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        self.make_section_label(section, "Quick Actions").pack(anchor="w", padx=20, pady=(16, 12))

        btn_row = ctk.CTkFrame(section, fg_color="transparent")
        btn_row.pack(anchor="w", padx=20, pady=(0, 16), fill="x")

        actions = [
            ("▶  Run Kometa", "runner", "primary"),
            ("🔌  Connections", "connections", "secondary"),
            ("📋  Edit Config", "yaml_editor", "secondary"),
            ("⚙️  Install / Update", "install", "secondary"),
        ]
        for text, page, style in actions:
            self.make_button(
                btn_row, text, lambda p=page: self.navigate(p), style=style, width=160
            ).pack(side="left", padx=(0, 10))

    def _build_info_card(self, parent):
        card = self.make_card(parent)
        card.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.make_section_label(card, "About Kometa Helper").pack(anchor="w", padx=20, pady=(16, 8))

        info_text = (
            "Kometa Helper makes it easy to install, configure, and manage Kometa on Windows.\n\n"
            "Use the sidebar to navigate:\n"
            "  •  Install  — download and set up Kometa automatically\n"
            "  •  Connections  — configure Plex, TMDb, Trakt, and other services\n"
            "  •  YAML Editor  — visually edit your config and collection files\n"
            "  •  Collections  — manage your collection file library\n"
            "  •  Run Kometa  — start runs with custom flags and see live output\n"
            "  •  Scheduler  — automate scheduled Kometa runs\n"
            "  •  Logs  — browse and search run logs\n"
            "  •  Backups  — restore previous YAML configurations"
        )
        ctk.CTkLabel(
            card,
            text=info_text,
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
            justify="left",
            anchor="w",
        ).pack(anchor="w", padx=20, pady=(0, 16))

    def on_show(self):
        self._refresh_status()

    def _refresh_status(self):
        # Kometa installed?
        if self.kometa.is_kometa_installed():
            version = self.kometa.get_installed_version() or "Installed"
            self._status_labels["status"].configure(text=version, text_color=COLORS["accent_green"])
        else:
            self._status_labels["status"].configure(text="Not Installed", text_color=COLORS["accent_red"])

        # Last run
        last_run = self.config.get("last_run")
        self._status_labels["last_run"].configure(
            text=str(last_run)[:16] if last_run else "Never",
            text_color=COLORS["text_secondary"],
        )

        # Config
        config_path = self.config.get_kometa_config_path()
        if config_path:
            self._status_labels["config"].configure(text="Found", text_color=COLORS["accent_green"])
        else:
            self._status_labels["config"].configure(text="Not Set", text_color=COLORS["accent_yellow"])

        # Libraries
        try:
            kometa_config = self.config.load_kometa_config()
            libs = kometa_config.get("libraries", {})
            self._status_labels["libraries"].configure(text=str(len(libs)), text_color=COLORS["accent"])
        except Exception:
            self._status_labels["libraries"].configure(text="0")
