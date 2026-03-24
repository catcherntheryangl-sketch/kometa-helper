"""
SettingsPage - App preferences, paths, and about info
"""

import tkinter.filedialog as fd
import customtkinter as ctk
from src.ui.pages.base_page import BasePage
from src.ui.theme import COLORS


class SettingsPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=32, pady=24)
        scroll.grid_columnconfigure(0, weight=1)

        self.make_page_header(scroll, "Settings", "Configure Kometa Helper preferences").grid(
            row=0, column=0, sticky="w", pady=(0, 24)
        )

        self._build_paths_section(scroll, row=1)
        self._build_notifications_section(scroll, row=2)
        self._build_appearance_section(scroll, row=3)
        self._build_about_section(scroll, row=4)
        self._build_save_row(scroll, row=5)

    def _build_paths_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        self.make_section_label(card, "Paths").pack(anchor="w", padx=20, pady=(16, 12))

        paths = [
            ("Kometa Install Dir", "kometa_install_dir", "Select Kometa Install Directory"),
            ("Kometa Config Dir",  "kometa_config_dir",  "Select Kometa Config Directory"),
            ("Python Executable",  "python_path",        "Select Python Executable"),
        ]

        self._path_entries = {}
        for label, key, dialog_title in paths:
            row_frame = ctk.CTkFrame(card, fg_color="transparent")
            row_frame.pack(anchor="w", padx=20, pady=(0, 10), fill="x")

            ctk.CTkLabel(
                row_frame, text=label,
                font=ctk.CTkFont("Segoe UI", 12),
                text_color=COLORS["text_secondary"],
                width=160, anchor="w",
            ).pack(side="left")

            entry = self.make_entry(row_frame, placeholder=f"Path to {label.lower()}", width=380)
            saved = self.config.get(key, "")
            if saved:
                entry.insert(0, saved)
            entry.pack(side="left", padx=(0, 8))
            self._path_entries[key] = entry

            ctk.CTkButton(
                row_frame, text="Browse",
                command=lambda k=key, t=dialog_title: self._browse_path(k, t),
                font=ctk.CTkFont("Segoe UI", 11),
                fg_color=COLORS["bg_input"],
                hover_color=COLORS["bg_hover"],
                text_color=COLORS["text_secondary"],
                corner_radius=6, width=70, height=32,
                border_width=1, border_color=COLORS["border"],
            ).pack(side="left")

        ctk.CTkFrame(card, height=8, fg_color="transparent").pack()

    def _build_notifications_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        self.make_section_label(card, "Notifications").pack(anchor="w", padx=20, pady=(16, 12))

        self._notif_complete = ctk.BooleanVar(value=self.config.get("notification_on_complete", True))
        self._notif_error    = ctk.BooleanVar(value=self.config.get("notification_on_error",    True))
        self._auto_update    = ctk.BooleanVar(value=self.config.get("auto_update_check",        True))

        toggles = [
            (self._notif_complete, "Notify when Kometa run completes"),
            (self._notif_error,    "Notify on run errors"),
            (self._auto_update,    "Check for Kometa updates on startup"),
        ]
        for var, label in toggles:
            ctk.CTkCheckBox(
                card, text=label, variable=var,
                font=ctk.CTkFont("Segoe UI", 12),
                text_color=COLORS["text_primary"],
                fg_color=COLORS["accent"], hover_color=COLORS["accent_dim"],
                checkmark_color="#000000", border_color=COLORS["border"],
            ).pack(anchor="w", padx=20, pady=4)

        ctk.CTkFrame(card, height=12, fg_color="transparent").pack()

    def _build_appearance_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        self.make_section_label(card, "Appearance").pack(anchor="w", padx=20, pady=(16, 12))

        row_frame = ctk.CTkFrame(card, fg_color="transparent")
        row_frame.pack(anchor="w", padx=20, pady=(0, 6))
        ctk.CTkLabel(
            row_frame, text="Theme",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
            width=120, anchor="w",
        ).pack(side="left")
        self._theme_menu = ctk.CTkOptionMenu(
            row_frame,
            values=["Dark", "Light", "System"],
            command=self._apply_theme,
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color=COLORS["bg_input"],
            button_color=COLORS["bg_hover"],
            text_color=COLORS["text_primary"],
            dropdown_fg_color=COLORS["bg_card"],
            width=160,
        )
        saved_theme = self.config.get("theme", "dark").capitalize()
        self._theme_menu.set(saved_theme)
        self._theme_menu.pack(side="left")

        ctk.CTkFrame(card, height=12, fg_color="transparent").pack()

    def _build_about_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        self.make_section_label(card, "About").pack(anchor="w", padx=20, pady=(16, 8))

        about_text = (
            "Kometa Helper  v1.0.0\n\n"
            "A Windows GUI wrapper for Kometa (Plex Metadata Manager).\n"
            "Makes installing, configuring, and running Kometa accessible to everyone.\n\n"
            "Built with Python + CustomTkinter.\n"
            "Kometa is developed by the Kometa Team: https://github.com/Kometa-Team/Kometa\n\n"
            "Kometa Helper is not affiliated with the official Kometa project."
        )
        ctk.CTkLabel(
            card,
            text=about_text,
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
            justify="left",
            anchor="w",
        ).pack(anchor="w", padx=20, pady=(0, 6))

        import webbrowser
        link_row = ctk.CTkFrame(card, fg_color="transparent")
        link_row.pack(anchor="w", padx=20, pady=(0, 16))

        for text, url in [
            ("Kometa Wiki ↗",    "https://kometa.wiki"),
            ("Kometa Discord ↗", "https://kometa.wiki/en/latest/discord/"),
            ("r/Kometa ↗",       "https://www.reddit.com/r/Kometa/"),
        ]:
            ctk.CTkButton(
                link_row, text=text,
                command=lambda u=url: webbrowser.open(u),
                font=ctk.CTkFont("Segoe UI", 11),
                fg_color="transparent",
                text_color=COLORS["accent"],
                hover_color=COLORS["bg_hover"],
                corner_radius=6,
                width=1, height=28,
            ).pack(side="left", padx=(0, 8))

    def _build_save_row(self, parent, row):
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.grid(row=row, column=0, sticky="w", pady=(0, 8))
        self.make_button(row_frame, "💾  Save Settings", self._save_settings, "primary", width=160).pack(side="left", padx=(0, 12))
        self._save_label = ctk.CTkLabel(
            row_frame, text="", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"]
        )
        self._save_label.pack(side="left")

    # ── Actions ───────────────────────────────────────────────────────────────

    def _browse_path(self, key: str, title: str):
        if "python" in key.lower():
            path = fd.askopenfilename(
                title=title,
                filetypes=[("Executable", "*.exe"), ("All files", "*.*")],
            )
        else:
            path = fd.askdirectory(title=title)
        if path:
            entry = self._path_entries[key]
            entry.delete(0, "end")
            entry.insert(0, path)

    def _apply_theme(self, theme: str):
        import customtkinter as ctk
        ctk.set_appearance_mode(theme.lower())
        self.config.set("theme", theme.lower())

    def _save_settings(self):
        for key, entry in self._path_entries.items():
            val = entry.get().strip()
            if val:
                self.config.set(key, val)

        self.config.set("notification_on_complete", self._notif_complete.get())
        self.config.set("notification_on_error",    self._notif_error.get())
        self.config.set("auto_update_check",        self._auto_update.get())
        self.config.set("theme", self._theme_menu.get().lower())

        self._save_label.configure(text="✓ Settings saved", text_color=COLORS["accent_green"])
        self.after(3000, lambda: self._save_label.configure(text=""))

    def on_show(self):
        for key, entry in self._path_entries.items():
            val = self.config.get(key, "")
            if val:
                entry.delete(0, "end")
                entry.insert(0, val)
