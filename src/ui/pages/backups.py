"""
BackupsPage - Browse and restore YAML backups
"""

import shutil
import customtkinter as ctk
from pathlib import Path
from src.ui.pages.base_page import BasePage
from src.ui.theme import COLORS


class BackupsPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=32, pady=(24, 16))
        top.grid_columnconfigure(1, weight=1)

        self.make_page_header(top, "Backups", "Restore previous YAML configurations").grid(row=0, column=0, sticky="w")
        self.make_button(top, "Refresh", self._refresh, "secondary", width=90).grid(row=0, column=1, sticky="e")

        # Split: backup list + preview
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 24))
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        list_panel = ctk.CTkFrame(main, width=280, fg_color=COLORS["bg_card"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        list_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        list_panel.grid_propagate(False)

        ctk.CTkLabel(list_panel, text="Backup Files", font=ctk.CTkFont("Segoe UI Semibold", 13), text_color=COLORS["text_secondary"]).pack(anchor="w", padx=12, pady=(12, 6))
        self._backup_list = ctk.CTkScrollableFrame(list_panel, fg_color="transparent")
        self._backup_list.pack(fill="both", expand=True, padx=4, pady=(0, 8))

        preview_panel = ctk.CTkFrame(main, fg_color=COLORS["bg_card"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        preview_panel.grid(row=0, column=1, sticky="nsew")
        preview_panel.grid_rowconfigure(2, weight=1)
        preview_panel.grid_columnconfigure(0, weight=1)

        self._preview_label = ctk.CTkLabel(preview_panel, text="Select a backup to preview", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_muted"])
        self._preview_label.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))

        self._restore_btn = self.make_button(preview_panel, "Restore This Backup", self._restore_selected, "primary", width=180)
        self._restore_btn.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self._restore_btn.configure(state="disabled")

        self._preview_box = ctk.CTkTextbox(
            preview_panel, font=ctk.CTkFont("Consolas", 11), fg_color=COLORS["bg_input"],
            text_color=COLORS["text_primary"], border_width=0, corner_radius=0, state="disabled"
        )
        self._preview_box.grid(row=2, column=0, sticky="nsew", padx=1, pady=(0, 1))

        self._selected_backup: Path | None = None
        self._refresh()

    def _refresh(self):
        for w in self._backup_list.winfo_children():
            w.destroy()
        backups = self.config.get_backups()
        if not backups:
            ctk.CTkLabel(self._backup_list, text="No backups yet.\nBackups are created\nautomatically on save.", font=ctk.CTkFont("Segoe UI", 11), text_color=COLORS["text_muted"], justify="center").pack(pady=20)
            return
        for b in backups:
            btn = ctk.CTkButton(
                self._backup_list, text=b.name, anchor="w",
                command=lambda p=b: self._select_backup(p),
                font=ctk.CTkFont("Consolas", 10),
                fg_color="transparent", text_color=COLORS["text_secondary"],
                hover_color=COLORS["bg_hover"], corner_radius=6, height=30,
            )
            btn.pack(fill="x", pady=1)

    def _select_backup(self, path: Path):
        self._selected_backup = path
        try:
            content = path.read_text(encoding="utf-8")
            self._preview_box.configure(state="normal")
            self._preview_box.delete("1.0", "end")
            self._preview_box.insert("1.0", content)
            self._preview_box.configure(state="disabled")
            self._preview_label.configure(text=path.name, text_color=COLORS["text_primary"])
            self._restore_btn.configure(state="normal")
        except Exception as e:
            self._preview_label.configure(text=f"Error: {e}", text_color=COLORS["accent_red"])

    def _restore_selected(self):
        if not self._selected_backup:
            return
        import tkinter.messagebox as mb
        if mb.askyesno("Restore Backup", f"Restore {self._selected_backup.name} as your config.yml?\n\nYour current config will be backed up first."):
            config_path = self.config.get_kometa_config_path()
            if config_path:
                self.config._backup_file(config_path)
                shutil.copy2(self._selected_backup, config_path)
                mb.showinfo("Restored", "Backup restored successfully.")
            else:
                mb.showerror("Error", "No config.yml path set. Go to Connections and generate a config first.")

    def on_show(self):
        self._refresh()
