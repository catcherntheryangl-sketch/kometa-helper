"""
YamlEditorPage - Visual + raw YAML editor with validation and file browser
"""

import tkinter.filedialog as fd
import customtkinter as ctk
from pathlib import Path
from src.ui.pages.base_page import BasePage
from src.ui.theme import COLORS
from src.utils.yaml_utils import yaml_to_string, string_to_yaml, get_friendly_yaml_error


class YamlEditorPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_file: Path | None = None
        self._unsaved = False
        self._build()

    def _build(self):
        # Top bar
        top = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top.pack(fill="x", padx=32, pady=(24, 0))
        top.pack_propagate(False)

        self.make_page_header(top, "YAML Editor", "Edit Kometa config and collection files").pack(side="left", anchor="w")

        btn_bar = ctk.CTkFrame(top, fg_color="transparent")
        btn_bar.pack(side="right", anchor="e")
        self.make_button(btn_bar, "📂 Open", self._open_file, "secondary", width=90).pack(side="left", padx=(0, 8))
        self.make_button(btn_bar, "💾 Save", self._save_file, "primary", width=90).pack(side="left", padx=(0, 8))
        self.make_button(btn_bar, "✓ Validate", self._validate, "secondary", width=100).pack(side="left")

        # File tab strip
        self._tab_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_panel"], height=40)
        self._tab_frame.pack(fill="x", padx=0, pady=(12, 0))

        self._new_file_btn = ctk.CTkButton(
            self._tab_frame,
            text="+ New File",
            command=self._new_file,
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color="transparent",
            text_color=COLORS["accent"],
            hover_color=COLORS["bg_hover"],
            width=90, height=36,
            corner_radius=0,
        )
        self._new_file_btn.pack(side="left", padx=(8, 0))

        self._file_label = ctk.CTkLabel(
            self._tab_frame,
            text="No file open",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_secondary"],
        )
        self._file_label.pack(side="left", padx=12)

        # Main editor area — left panel (quick fields) + right (raw YAML)
        editor_area = ctk.CTkFrame(self, fg_color="transparent")
        editor_area.pack(fill="both", expand=True, padx=32, pady=16)
        editor_area.grid_columnconfigure(0, weight=0)
        editor_area.grid_columnconfigure(1, weight=1)
        editor_area.grid_rowconfigure(0, weight=1)

        # Left panel: quick edit fields
        self._left_panel = ctk.CTkFrame(
            editor_area,
            width=280,
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        self._left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        self._left_panel.grid_propagate(False)
        self._build_left_panel()

        # Right panel: raw YAML textbox
        right_panel = ctk.CTkFrame(editor_area, fg_color=COLORS["bg_card"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        editor_header = ctk.CTkFrame(right_panel, fg_color="transparent", height=44)
        editor_header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 0))

        ctk.CTkLabel(
            editor_header,
            text="Raw YAML",
            font=ctk.CTkFont("Segoe UI Semibold", 13),
            text_color=COLORS["text_secondary"],
        ).pack(side="left")

        self._validation_label = ctk.CTkLabel(
            editor_header,
            text="",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_secondary"],
        )
        self._validation_label.pack(side="right")

        self._editor = ctk.CTkTextbox(
            right_panel,
            font=ctk.CTkFont("Consolas", 12),
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_primary"],
            border_width=0,
            corner_radius=0,
            wrap="none",
        )
        self._editor.grid(row=1, column=0, sticky="nsew", padx=1, pady=(0, 1))
        self._editor.bind("<KeyRelease>", self._on_edit)

        # Status bar
        self._status_bar = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=COLORS["text_muted"],
            anchor="w",
        )
        self._status_bar.pack(fill="x", padx=32, pady=(0, 8))

    def _build_left_panel(self):
        scroll = ctk.CTkScrollableFrame(self._left_panel, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=0, pady=0)

        ctk.CTkLabel(
            scroll,
            text="Quick Edit",
            font=ctk.CTkFont("Segoe UI Semibold", 13),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=16, pady=(16, 4))

        ctk.CTkLabel(
            scroll,
            text="Common fields from your config",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(0, 12))

        # Plex
        ctk.CTkLabel(scroll, text="Plex URL", font=ctk.CTkFont("Segoe UI", 11), text_color=COLORS["text_secondary"]).pack(anchor="w", padx=16, pady=(6, 2))
        self._qe_plex_url = ctk.CTkEntry(scroll, font=ctk.CTkFont("Segoe UI", 11), fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text_primary"], placeholder_text="http://localhost:32400", width=240, corner_radius=6)
        self._qe_plex_url.pack(anchor="w", padx=16, pady=(0, 6))

        ctk.CTkLabel(scroll, text="Plex Token", font=ctk.CTkFont("Segoe UI", 11), text_color=COLORS["text_secondary"]).pack(anchor="w", padx=16, pady=(2, 2))
        self._qe_plex_token = ctk.CTkEntry(scroll, show="*", font=ctk.CTkFont("Segoe UI", 11), fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text_primary"], placeholder_text="token", width=240, corner_radius=6)
        self._qe_plex_token.pack(anchor="w", padx=16, pady=(0, 6))

        ctk.CTkLabel(scroll, text="TMDb API Key", font=ctk.CTkFont("Segoe UI", 11), text_color=COLORS["text_secondary"]).pack(anchor="w", padx=16, pady=(2, 2))
        self._qe_tmdb = ctk.CTkEntry(scroll, show="*", font=ctk.CTkFont("Segoe UI", 11), fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text_primary"], placeholder_text="api-key", width=240, corner_radius=6)
        self._qe_tmdb.pack(anchor="w", padx=16, pady=(0, 12))

        ctk.CTkFrame(scroll, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=16, pady=(0, 12))

        self.make_button(scroll, "Apply to YAML →", self._apply_quick_edit, "primary", width=240).pack(anchor="w", padx=16, pady=(0, 12))

        ctk.CTkLabel(
            scroll,
            text="Templates",
            font=ctk.CTkFont("Segoe UI Semibold", 12),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=16, pady=(4, 8))

        templates = [
            ("Blank config.yml", "config"),
            ("Collection file", "collection"),
            ("Overlay file", "overlay"),
        ]
        for name, key in templates:
            ctk.CTkButton(
                scroll,
                text=name,
                command=lambda k=key: self._load_template(k),
                font=ctk.CTkFont("Segoe UI", 11),
                fg_color="transparent",
                text_color=COLORS["accent"],
                hover_color=COLORS["bg_hover"],
                anchor="w",
                width=240,
                height=30,
                corner_radius=6,
            ).pack(anchor="w", padx=16, pady=2)

    # ── File ops ──────────────────────────────────────────────────────────────

    def _open_file(self):
        path = fd.askopenfilename(
            title="Open YAML File",
            filetypes=[("YAML files", "*.yml *.yaml"), ("All files", "*.*")],
            initialdir=self.config.get("kometa_config_dir") or "~",
        )
        if path:
            self._load_file(Path(path))

    def _load_file(self, path: Path):
        try:
            content = path.read_text(encoding="utf-8")
            self._editor.delete("1.0", "end")
            self._editor.insert("1.0", content)
            self._current_file = path
            self._file_label.configure(text=path.name)
            self._status_bar.configure(text=f"Opened: {path}", text_color=COLORS["text_muted"])
            self._unsaved = False
            self._auto_populate_quick_edit(content)
        except Exception as e:
            self._status_bar.configure(text=f"Error opening file: {e}", text_color=COLORS["accent_red"])

    def _save_file(self):
        content = self._editor.get("1.0", "end-1c")
        ok, err = self.config.validate_yaml_string(content)
        if not ok:
            self._validation_label.configure(
                text=f"⚠ Fix YAML errors before saving",
                text_color=COLORS["accent_red"],
            )
            return

        if self._current_file:
            try:
                if self._current_file.exists():
                    self.config._backup_file(self._current_file)
                self._current_file.write_text(content, encoding="utf-8")
                self._unsaved = False
                self._status_bar.configure(text=f"Saved: {self._current_file}", text_color=COLORS["accent_green"])
                self._validation_label.configure(text="✓ Saved", text_color=COLORS["accent_green"])
            except Exception as e:
                self._status_bar.configure(text=f"Save error: {e}", text_color=COLORS["accent_red"])
        else:
            path = fd.asksaveasfilename(
                defaultextension=".yml",
                filetypes=[("YAML files", "*.yml")],
                initialdir=self.config.get("kometa_config_dir") or "~",
            )
            if path:
                self._current_file = Path(path)
                self._save_file()

    def _new_file(self):
        self._editor.delete("1.0", "end")
        self._current_file = None
        self._file_label.configure(text="Untitled.yml")
        self._unsaved = False

    def _validate(self):
        content = self._editor.get("1.0", "end-1c")
        ok, err = self.config.validate_yaml_string(content)
        if ok:
            self._validation_label.configure(text="✓ Valid YAML", text_color=COLORS["accent_green"])
            self._status_bar.configure(text="YAML is valid", text_color=COLORS["accent_green"])
        else:
            friendly = get_friendly_yaml_error(err)
            self._validation_label.configure(text="✗ Invalid YAML", text_color=COLORS["accent_red"])
            self._status_bar.configure(text=friendly, text_color=COLORS["accent_red"])

    def _load_template(self, key: str):
        from src.utils.yaml_utils import KOMETA_CONFIG_TEMPLATE, COLLECTION_TEMPLATE, OVERLAY_TEMPLATE
        templates = {
            "config": KOMETA_CONFIG_TEMPLATE,
            "collection": COLLECTION_TEMPLATE,
            "overlay": OVERLAY_TEMPLATE,
        }
        data = templates.get(key, {})
        content = yaml_to_string(data)
        self._editor.delete("1.0", "end")
        self._editor.insert("1.0", content)
        self._file_label.configure(text=f"Template: {key}.yml")
        self._current_file = None

    def _on_edit(self, event=None):
        self._unsaved = True
        self._validation_label.configure(text="", text_color=COLORS["text_secondary"])

    def _apply_quick_edit(self):
        content = self._editor.get("1.0", "end-1c")
        data, err = string_to_yaml(content)
        if err:
            self._status_bar.configure(text=get_friendly_yaml_error(err), text_color=COLORS["accent_red"])
            return
        if not isinstance(data, dict):
            data = {}

        plex_url = self._qe_plex_url.get().strip()
        plex_token = self._qe_plex_token.get().strip()
        tmdb_key = self._qe_tmdb.get().strip()

        if plex_url or plex_token:
            if "plex" not in data:
                data["plex"] = {}
            if plex_url:
                data["plex"]["url"] = plex_url
            if plex_token:
                data["plex"]["token"] = plex_token

        if tmdb_key:
            if "tmdb" not in data:
                data["tmdb"] = {}
            data["tmdb"]["apikey"] = tmdb_key

        self._editor.delete("1.0", "end")
        self._editor.insert("1.0", yaml_to_string(data))
        self._status_bar.configure(text="Quick edit applied", text_color=COLORS["accent_green"])

    def _auto_populate_quick_edit(self, content: str):
        data, _ = string_to_yaml(content)
        if not isinstance(data, dict):
            return
        plex = data.get("plex", {})
        if isinstance(plex, dict):
            url = plex.get("url", "")
            token = plex.get("token", "")
            if url:
                self._qe_plex_url.delete(0, "end")
                self._qe_plex_url.insert(0, url)
            if token:
                self._qe_plex_token.delete(0, "end")
                self._qe_plex_token.insert(0, token)
        tmdb = data.get("tmdb", {})
        if isinstance(tmdb, dict):
            key = tmdb.get("apikey", "")
            if key:
                self._qe_tmdb.delete(0, "end")
                self._qe_tmdb.insert(0, key)

    def on_show(self):
        if not self._current_file:
            config_path = self.config.get_kometa_config_path()
            if config_path:
                self._load_file(config_path)
