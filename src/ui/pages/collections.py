"""
CollectionsPage - Browse, enable/disable, and manage collection YAML files
"""

import tkinter.filedialog as fd
import customtkinter as ctk
from pathlib import Path
from src.ui.pages.base_page import BasePage
from src.ui.theme import COLORS
from src.utils.yaml_utils import DEFAULTS_COLLECTIONS, DEFAULTS_OVERLAYS, yaml_to_string


class CollectionsPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build()

    def _build(self):
        # Top bar
        top = ctk.CTkFrame(self, fg_color="transparent", height=70)
        top.pack(fill="x", padx=32, pady=(24, 0))
        top.pack_propagate(False)

        self.make_page_header(top, "Collections & Overlays", "Manage your collection and overlay files").pack(side="left", anchor="w")

        btn_bar = ctk.CTkFrame(top, fg_color="transparent")
        btn_bar.pack(side="right", anchor="e")
        self.make_button(btn_bar, "+ Add File", self._add_file, "primary", width=110).pack(side="left", padx=(0, 8))
        self.make_button(btn_bar, "Refresh", self._refresh, "secondary", width=90).pack(side="left")

        # Tabs: Libraries | Defaults Picker
        tab_bar = ctk.CTkFrame(self, fg_color=COLORS["bg_panel"], height=44)
        tab_bar.pack(fill="x", pady=(12, 0))

        self._active_tab = ctk.StringVar(value="libraries")
        for label, key in [("📁  Your Files", "libraries"), ("🎯  Kometa Defaults", "defaults")]:
            ctk.CTkButton(
                tab_bar,
                text=label,
                command=lambda k=key: self._switch_tab(k),
                font=ctk.CTkFont("Segoe UI Semibold", 12),
                fg_color=COLORS["nav_active_bg"] if key == "libraries" else "transparent",
                text_color=COLORS["accent"] if key == "libraries" else COLORS["text_secondary"],
                hover_color=COLORS["bg_hover"],
                corner_radius=0,
                height=44,
                width=160,
            ).pack(side="left")

        self._tab_buttons = {}

        # Content area
        self._content = ctk.CTkFrame(self, fg_color="transparent")
        self._content.pack(fill="both", expand=True, padx=32, pady=16)

        self._libraries_view = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        self._defaults_view = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        self._libraries_view.pack(fill="both", expand=True)

        self._build_defaults_view()

    def _switch_tab(self, key: str):
        if key == "libraries":
            self._defaults_view.pack_forget()
            self._libraries_view.pack(fill="both", expand=True)
            self._refresh()
        else:
            self._libraries_view.pack_forget()
            self._defaults_view.pack(fill="both", expand=True)

    def _refresh(self):
        for widget in self._libraries_view.winfo_children():
            widget.destroy()

        cfg_dir = self.config.get("kometa_config_dir")
        if not cfg_dir:
            ctk.CTkLabel(
                self._libraries_view,
                text="No Kometa config directory set. Go to Install to set it up.",
                font=ctk.CTkFont("Segoe UI", 13),
                text_color=COLORS["text_secondary"],
            ).pack(pady=40)
            return

        files = self.config.get_collection_files()
        yml_files = [f for f in files if f.name != "config.yml"]

        if not yml_files:
            card = self.make_card(self._libraries_view)
            card.pack(fill="x", pady=(0, 12))
            ctk.CTkLabel(
                card,
                text="No collection or overlay files found.\n\nCreate a new file or use the Kometa Defaults tab to enable built-in collections.",
                font=ctk.CTkFont("Segoe UI", 13),
                text_color=COLORS["text_secondary"],
                justify="center",
            ).pack(pady=40)
            return

        for file_path in yml_files:
            self._build_file_card(self._libraries_view, file_path)

    def _build_file_card(self, parent, file_path: Path):
        card = self.make_card(parent)
        card.pack(fill="x", pady=(0, 10))

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=12)

        # Icon
        icon = "📋" if "collection" in file_path.name.lower() else "🎨" if "overlay" in file_path.name.lower() else "📄"
        ctk.CTkLabel(
            row,
            text=icon,
            font=ctk.CTkFont("Segoe UI", 18),
        ).pack(side="left", padx=(0, 10))

        # Info
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            info,
            text=file_path.name,
            font=ctk.CTkFont("Segoe UI Semibold", 13),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        # Try to get collection count
        try:
            import yaml
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            collections = data.get("collections", {})
            overlays = data.get("overlays", {})
            count_text = []
            if collections:
                count_text.append(f"{len(collections)} collection(s)")
            if overlays:
                count_text.append(f"{len(overlays)} overlay(s)")
            detail = ", ".join(count_text) if count_text else "Empty file"
        except Exception:
            detail = "Could not parse"

        ctk.CTkLabel(
            info,
            text=detail,
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

        # Buttons
        btn_group = ctk.CTkFrame(row, fg_color="transparent")
        btn_group.pack(side="right")

        ctk.CTkButton(
            btn_group,
            text="Edit",
            command=lambda p=file_path: self._edit_file(p),
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color=COLORS["bg_input"],
            hover_color=COLORS["bg_hover"],
            text_color=COLORS["text_primary"],
            corner_radius=6,
            width=60,
            height=30,
            border_width=1,
            border_color=COLORS["border"],
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_group,
            text="Delete",
            command=lambda p=file_path: self._delete_file(p),
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color="transparent",
            hover_color=COLORS["accent_red"] + "33",
            text_color=COLORS["accent_red"],
            corner_radius=6,
            width=60,
            height=30,
            border_width=1,
            border_color=COLORS["accent_red"] + "55",
        ).pack(side="left")

    def _build_defaults_view(self):
        scroll = self._defaults_view

        self.make_page_header(scroll, "Kometa Defaults", "Enable built-in collection and overlay files").pack(anchor="w", pady=(0, 16))

        ctk.CTkLabel(
            scroll,
            text="These are the built-in Kometa defaults. Enabling them will add them to your config.yml libraries.",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
            wraplength=700,
            justify="left",
        ).pack(anchor="w", pady=(0, 16))

        # Collections
        ctk.CTkLabel(
            scroll,
            text="Default Collections",
            font=ctk.CTkFont("Segoe UI Semibold", 14),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 8))

        self._default_collection_vars = {}
        grid = ctk.CTkFrame(scroll, fg_color="transparent")
        grid.pack(anchor="w", fill="x")

        for i, name in enumerate(DEFAULTS_COLLECTIONS):
            short = name.replace("defaults/collections/", "").replace("/", " › ")
            var = ctk.BooleanVar(value=False)
            self._default_collection_vars[name] = var
            ctk.CTkCheckBox(
                grid,
                text=short,
                variable=var,
                font=ctk.CTkFont("Segoe UI", 11),
                text_color=COLORS["text_primary"],
                fg_color=COLORS["accent"],
                hover_color=COLORS["accent_dim"],
                checkmark_color="#000000",
                border_color=COLORS["border"],
            ).grid(row=i // 3, column=i % 3, sticky="w", padx=8, pady=3)

        # Overlays
        ctk.CTkLabel(
            scroll,
            text="Default Overlays",
            font=ctk.CTkFont("Segoe UI Semibold", 14),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(16, 8))

        self._default_overlay_vars = {}
        grid2 = ctk.CTkFrame(scroll, fg_color="transparent")
        grid2.pack(anchor="w", fill="x")

        for i, name in enumerate(DEFAULTS_OVERLAYS):
            short = name.replace("defaults/overlays/", "")
            var = ctk.BooleanVar(value=False)
            self._default_overlay_vars[name] = var
            ctk.CTkCheckBox(
                grid2,
                text=short,
                variable=var,
                font=ctk.CTkFont("Segoe UI", 11),
                text_color=COLORS["text_primary"],
                fg_color=COLORS["accent"],
                hover_color=COLORS["accent_dim"],
                checkmark_color="#000000",
                border_color=COLORS["border"],
            ).grid(row=i // 3, column=i % 3, sticky="w", padx=8, pady=3)

        ctk.CTkFrame(scroll, height=16, fg_color="transparent").pack()

        # Library selector + apply
        apply_row = ctk.CTkFrame(scroll, fg_color="transparent")
        apply_row.pack(anchor="w", pady=(8, 0))

        ctk.CTkLabel(apply_row, text="Apply to library:", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"]).pack(side="left", padx=(0, 8))
        self._library_selector = ctk.CTkOptionMenu(
            apply_row,
            values=["— Select Library —"],
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color=COLORS["bg_input"],
            button_color=COLORS["bg_hover"],
            text_color=COLORS["text_primary"],
            dropdown_fg_color=COLORS["bg_card"],
            width=220,
        )
        self._library_selector.pack(side="left", padx=(0, 12))
        self.make_button(apply_row, "Apply to Config", self._apply_defaults, "primary", width=150).pack(side="left")

    def _edit_file(self, path: Path):
        """Open in YAML editor."""
        page = self._get_page("yaml_editor")
        if page:
            page._load_file(path)
        self.navigate("yaml_editor")

    def _get_page(self, key):
        parent = self.master
        while parent:
            if hasattr(parent, "_pages"):
                return parent._pages.get(key)
            parent = getattr(parent, "master", None)
        return None

    def _delete_file(self, path: Path):
        import tkinter.messagebox as mb
        if mb.askyesno("Delete File", f"Delete {path.name}?\n\nA backup will be created first."):
            self.config._backup_file(path)
            path.unlink()
            self._refresh()

    def _add_file(self):
        path = fd.askopenfilename(
            title="Add YAML File",
            filetypes=[("YAML files", "*.yml *.yaml")],
        )
        if path:
            import shutil
            dest = Path(self.config.get("kometa_config_dir", ".")) / Path(path).name
            shutil.copy2(path, dest)
            self._refresh()

    def _apply_defaults(self):
        lib_name = self._library_selector.get()
        if lib_name.startswith("—"):
            return
        enabled_collections = [k for k, v in self._default_collection_vars.items() if v.get()]
        enabled_overlays = [k for k, v in self._default_overlay_vars.items() if v.get()]

        try:
            cfg = self.config.load_kometa_config()
            if "libraries" not in cfg:
                cfg["libraries"] = {}
            if lib_name not in cfg["libraries"]:
                cfg["libraries"][lib_name] = {}
            lib = cfg["libraries"][lib_name]

            if enabled_collections:
                existing = lib.get("collection_files", [])
                new_entries = [{"default": c} for c in enabled_collections]
                lib["collection_files"] = existing + new_entries

            if enabled_overlays:
                existing = lib.get("overlay_files", [])
                new_entries = [{"default": o} for o in enabled_overlays]
                lib["overlay_files"] = existing + new_entries

            self.config.save_kometa_config(cfg)
        except Exception as e:
            print(f"Error applying defaults: {e}")

    def on_show(self):
        self._refresh()
        # Populate library selector
        try:
            cfg = self.config.load_kometa_config()
            libs = list(cfg.get("libraries", {}).keys())
            if libs:
                self._library_selector.configure(values=libs)
                self._library_selector.set(libs[0])
        except Exception:
            pass
