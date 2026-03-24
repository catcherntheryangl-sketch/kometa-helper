"""
ConnectionsPage - Configure and test all service connections
"""

import threading
import webbrowser
import customtkinter as ctk
from src.ui.pages.base_page import BasePage
from src.ui.theme import COLORS


SERVICE_LINKS = {
    "tmdb":    ("Get TMDb API Key", "https://www.themoviedb.org/settings/api"),
    "trakt":   ("Get Trakt API Keys", "https://trakt.tv/oauth/applications/new"),
    "mdblist": ("Get MDBList API Key", "https://mdblist.com/preferences/"),
    "radarr":  ("Radarr Settings Guide", "https://wiki.servarr.com/radarr"),
    "sonarr":  ("Sonarr Settings Guide", "https://wiki.servarr.com/sonarr"),
}


class ConnectionsPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=32, pady=24)
        scroll.grid_columnconfigure(0, weight=1)

        self.make_page_header(
            scroll, "Connections", "Connect Kometa to your media services"
        ).grid(row=0, column=0, sticky="w", pady=(0, 24))

        self._build_plex_section(scroll, row=1)
        self._build_tmdb_section(scroll, row=2)
        self._build_trakt_section(scroll, row=3)
        self._build_mdblist_section(scroll, row=4)
        self._build_radarr_section(scroll, row=5)
        self._build_sonarr_section(scroll, row=6)
        self._build_save_row(scroll, row=7)

    def _build_plex_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))

        self._section_header(card, "🎬  Plex", "https://www.plex.tv/claim")

        ctk.CTkLabel(
            card,
            text="To find your Plex Token: In Plex Web, open any item, click '..', 'Get Info', then 'View XML'. The token appears in the URL after X-Plex-Token=",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_secondary"],
            wraplength=700,
            justify="left",
        ).pack(anchor="w", padx=20, pady=(0, 12))

        self._plex_url = self._field_row(card, "Plex URL", "http://localhost:32400", width=380)
        self._plex_token = self._field_row(card, "Plex Token", "your-plex-token", show="*", width=380)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(anchor="w", padx=20, pady=(4, 16))
        self.make_button(btn_row, "Test Connection", lambda: self._test_plex(), "primary", width=140).pack(side="left", padx=(0, 12))
        self._plex_status = ctk.CTkLabel(btn_row, text="", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"])
        self._plex_status.pack(side="left")

        # Libraries list
        self._plex_libs_frame = ctk.CTkFrame(card, fg_color=COLORS["bg_input"], corner_radius=6)
        self._plex_libs_frame.pack(fill="x", padx=20, pady=(0, 16))
        ctk.CTkLabel(
            self._plex_libs_frame,
            text="Connect and test to see your Plex libraries",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_muted"],
        ).pack(padx=12, pady=10)

    def _build_tmdb_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        self._section_header(card, "🎥  TMDb", SERVICE_LINKS["tmdb"][1], SERVICE_LINKS["tmdb"][0])
        self._tmdb_key = self._field_row(card, "API Key", "your-tmdb-api-key", show="*", width=420)
        self._tmdb_language = self._field_row(card, "Language", "en", width=100)
        self._tmdb_region = self._field_row(card, "Region", "US", width=100)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(anchor="w", padx=20, pady=(4, 16))
        self.make_button(btn_row, "Test Connection", lambda: self._test_tmdb(), "primary", width=140).pack(side="left", padx=(0, 12))
        self._tmdb_status = ctk.CTkLabel(btn_row, text="", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"])
        self._tmdb_status.pack(side="left")

    def _build_trakt_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        self._section_header(card, "📺  Trakt", SERVICE_LINKS["trakt"][1], SERVICE_LINKS["trakt"][0])
        ctk.CTkLabel(
            card,
            text="Create a new Trakt application to get your Client ID and Secret.",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=20, pady=(0, 10))
        self._trakt_id = self._field_row(card, "Client ID", "your-trakt-client-id", width=420)
        self._trakt_secret = self._field_row(card, "Client Secret", "your-trakt-client-secret", show="*", width=420)
        ctk.CTkFrame(card, height=8, fg_color="transparent").pack()

    def _build_mdblist_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        self._section_header(card, "📊  MDBList", SERVICE_LINKS["mdblist"][1], SERVICE_LINKS["mdblist"][0])
        self._mdblist_key = self._field_row(card, "API Key", "your-mdblist-api-key", show="*", width=420)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(anchor="w", padx=20, pady=(4, 16))
        self.make_button(btn_row, "Test Connection", lambda: self._test_mdblist(), "primary", width=140).pack(side="left", padx=(0, 12))
        self._mdblist_status = ctk.CTkLabel(btn_row, text="", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"])
        self._mdblist_status.pack(side="left")

    def _build_radarr_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        self._section_header(card, "🎬  Radarr (optional)", SERVICE_LINKS["radarr"][1], SERVICE_LINKS["radarr"][0])
        self._radarr_url = self._field_row(card, "URL", "http://localhost:7878", width=320)
        self._radarr_key = self._field_row(card, "API Key", "your-radarr-api-key", show="*", width=380)
        ctk.CTkFrame(card, height=8, fg_color="transparent").pack()

    def _build_sonarr_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        self._section_header(card, "📺  Sonarr (optional)", SERVICE_LINKS["sonarr"][1], SERVICE_LINKS["sonarr"][0])
        self._sonarr_url = self._field_row(card, "URL", "http://localhost:8989", width=320)
        self._sonarr_key = self._field_row(card, "API Key", "your-sonarr-api-key", show="*", width=380)
        ctk.CTkFrame(card, height=8, fg_color="transparent").pack()

    def _build_save_row(self, parent, row):
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.grid(row=row, column=0, sticky="ew", pady=(8, 0))
        self.make_button(row_frame, "💾  Save All Connections", self._save_all, "primary", width=220).pack(side="left", padx=(0, 12))
        self.make_button(row_frame, "Generate config.yml", self._generate_config, "secondary", width=180).pack(side="left")
        self._save_status = ctk.CTkLabel(row_frame, text="", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"])
        self._save_status.pack(side="left", padx=12)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _section_header(self, card, title: str, link_url: str = "", link_text: str = ""):
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=(16, 8))
        ctk.CTkLabel(
            row, text=title,
            font=ctk.CTkFont("Segoe UI Semibold", 14),
            text_color=COLORS["text_primary"],
        ).pack(side="left")
        if link_url and link_text:
            ctk.CTkButton(
                row,
                text=f"↗ {link_text}",
                command=lambda: webbrowser.open(link_url),
                font=ctk.CTkFont("Segoe UI", 11),
                fg_color="transparent",
                text_color=COLORS["accent"],
                hover_color=COLORS["bg_hover"],
                width=1, height=28,
            ).pack(side="right")

    def _field_row(self, card, label: str, placeholder: str, show=None, width=320) -> ctk.CTkEntry:
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(anchor="w", padx=20, pady=(0, 8))
        ctk.CTkLabel(
            row, text=label,
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
            width=120,
            anchor="w",
        ).pack(side="left")
        entry = self.make_entry(row, placeholder, show=show, width=width)
        entry.pack(side="left")
        return entry

    def _set_entry(self, entry: ctk.CTkEntry, value: str):
        if value:
            entry.delete(0, "end")
            entry.insert(0, value)

    def on_show(self):
        """Populate fields from saved settings."""
        self._set_entry(self._plex_url, self.config.get("plex_url", ""))
        self._set_entry(self._plex_token, self.config.get("plex_token", ""))
        self._set_entry(self._tmdb_key, self.config.get("tmdb_api_key", ""))
        self._set_entry(self._tmdb_language, self.config.get("tmdb_language", "en"))
        self._set_entry(self._tmdb_region, self.config.get("tmdb_region", "US"))
        self._set_entry(self._trakt_id, self.config.get("trakt_client_id", ""))
        self._set_entry(self._trakt_secret, self.config.get("trakt_client_secret", ""))
        self._set_entry(self._mdblist_key, self.config.get("mdblist_api_key", ""))
        self._set_entry(self._radarr_url, self.config.get("radarr_url", ""))
        self._set_entry(self._radarr_key, self.config.get("radarr_api_key", ""))
        self._set_entry(self._sonarr_url, self.config.get("sonarr_url", ""))
        self._set_entry(self._sonarr_key, self.config.get("sonarr_api_key", ""))

    def _test_plex(self):
        url = self._plex_url.get().strip()
        token = self._plex_token.get().strip()
        if not url or not token:
            self._plex_status.configure(text="Enter URL and token first", text_color=COLORS["accent_yellow"])
            return
        self._plex_status.configure(text="Testing...", text_color=COLORS["text_secondary"])

        def _run():
            ok, msg = self.kometa.test_plex_connection(url, token)
            libs = self.kometa.get_plex_libraries(url, token) if ok else []

            def _done():
                if ok:
                    self._plex_status.configure(text=f"✓ {msg}", text_color=COLORS["accent_green"])
                    self._show_plex_libraries(libs)
                else:
                    self._plex_status.configure(text=f"✗ {msg}", text_color=COLORS["accent_red"])
            self.after(0, _done)
        threading.Thread(target=_run, daemon=True).start()

    def _show_plex_libraries(self, libs: list):
        for w in self._plex_libs_frame.winfo_children():
            w.destroy()
        if not libs:
            ctk.CTkLabel(self._plex_libs_frame, text="No libraries found", font=ctk.CTkFont("Segoe UI", 11), text_color=COLORS["text_muted"]).pack(padx=12, pady=8)
            return
        ctk.CTkLabel(
            self._plex_libs_frame,
            text=f"Found {len(libs)} libraries:",
            font=ctk.CTkFont("Segoe UI Semibold", 11),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=12, pady=(8, 4))
        for lib in libs:
            icon = "🎬" if lib["type"] == "movie" else "📺" if lib["type"] == "show" else "🎵"
            ctk.CTkLabel(
                self._plex_libs_frame,
                text=f"  {icon}  {lib['title']}  ({lib['type']})",
                font=ctk.CTkFont("Segoe UI", 11),
                text_color=COLORS["text_primary"],
            ).pack(anchor="w", padx=12)
        ctk.CTkFrame(self._plex_libs_frame, height=6, fg_color="transparent").pack()

    def _test_tmdb(self):
        key = self._tmdb_key.get().strip()
        if not key:
            self._tmdb_status.configure(text="Enter API key first", text_color=COLORS["accent_yellow"])
            return
        self._tmdb_status.configure(text="Testing...", text_color=COLORS["text_secondary"])

        def _run():
            ok, msg = self.kometa.test_tmdb_connection(key)
            self.after(0, lambda: self._tmdb_status.configure(
                text=f"✓ {msg}" if ok else f"✗ {msg}",
                text_color=COLORS["accent_green"] if ok else COLORS["accent_red"],
            ))
        threading.Thread(target=_run, daemon=True).start()

    def _test_mdblist(self):
        key = self._mdblist_key.get().strip()
        if not key:
            self._mdblist_status.configure(text="Enter API key first", text_color=COLORS["accent_yellow"])
            return
        self._mdblist_status.configure(text="Testing...", text_color=COLORS["text_secondary"])

        def _run():
            ok, msg = self.kometa.test_mdblist_connection(key)
            self.after(0, lambda: self._mdblist_status.configure(
                text=f"✓ {msg}" if ok else f"✗ {msg}",
                text_color=COLORS["accent_green"] if ok else COLORS["accent_red"],
            ))
        threading.Thread(target=_run, daemon=True).start()

    def _save_all(self):
        self.config.set("plex_url", self._plex_url.get().strip())
        self.config.set("plex_token", self._plex_token.get().strip())
        self.config.set("tmdb_api_key", self._tmdb_key.get().strip())
        self.config.set("tmdb_language", self._tmdb_language.get().strip() or "en")
        self.config.set("tmdb_region", self._tmdb_region.get().strip() or "US")
        self.config.set("trakt_client_id", self._trakt_id.get().strip())
        self.config.set("trakt_client_secret", self._trakt_secret.get().strip())
        self.config.set("mdblist_api_key", self._mdblist_key.get().strip())
        self.config.set("radarr_url", self._radarr_url.get().strip())
        self.config.set("radarr_api_key", self._radarr_key.get().strip())
        self.config.set("sonarr_url", self._sonarr_url.get().strip())
        self.config.set("sonarr_api_key", self._sonarr_key.get().strip())
        self._save_status.configure(text="✓ Saved", text_color=COLORS["accent_green"])
        self.after(3000, lambda: self._save_status.configure(text=""))

    def _generate_config(self):
        """Write a config.yml from current connections."""
        from src.utils.yaml_utils import build_config_yml
        plex_url = self._plex_url.get().strip()
        plex_token = self._plex_token.get().strip()
        tmdb_key = self._tmdb_key.get().strip()
        if not plex_url or not plex_token or not tmdb_key:
            self._save_status.configure(text="Plex URL, Token, and TMDb key are required", text_color=COLORS["accent_yellow"])
            return
        self._save_all()
        cfg = build_config_yml(plex_url, plex_token, tmdb_key, libraries=[])
        try:
            self.config.save_kometa_config(cfg)
            self._save_status.configure(text="✓ config.yml generated!", text_color=COLORS["accent_green"])
        except Exception as e:
            self._save_status.configure(text=f"Error: {e}", text_color=COLORS["accent_red"])
