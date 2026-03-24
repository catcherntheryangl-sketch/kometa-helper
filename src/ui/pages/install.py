"""
InstallPage - Guided Kometa installation and update management
"""

import threading
import tkinter.filedialog as fd
import customtkinter as ctk
from src.ui.pages.base_page import BasePage
from src.ui.theme import COLORS


class InstallPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=32, pady=24)
        scroll.grid_columnconfigure(0, weight=1)

        self.make_page_header(
            scroll, "Install & Update", "Set up Kometa on your Windows machine"
        ).grid(row=0, column=0, sticky="w", pady=(0, 24))

        # Step 1 — Python check
        self._build_python_step(scroll, row=1)
        # Step 2 — Git check
        self._build_git_step(scroll, row=2)
        # Step 3 — Install location
        self._build_install_step(scroll, row=3)
        # Update section
        self._build_update_section(scroll, row=4)
        # Log output
        self._build_log_area(scroll, row=5)

    def _build_python_step(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(
            header,
            text="Step 1 — Python",
            font=ctk.CTkFont("Segoe UI Semibold", 14),
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        self._python_badge = ctk.CTkLabel(
            header,
            text=" Checking... ",
            font=ctk.CTkFont("Segoe UI Semibold", 10),
            text_color=COLORS["accent_yellow"],
            fg_color=COLORS["accent_yellow"] + "22",
            corner_radius=4,
        )
        self._python_badge.pack(side="right")

        self._python_detail = ctk.CTkLabel(
            card,
            text="Kometa requires Python 3.10 or newer.",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
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
            height=36,
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
            text_color=COLORS["text_primary"],
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

        self._git_detail = ctk.CTkLabel(
            card,
            text="Git is required to clone and update Kometa from GitHub.",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        )
        self._git_detail.pack(anchor="w", padx=20, pady=(0, 4))

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(anchor="w", padx=20, pady=(0, 16))
        self.make_button(btn_row, "Check Git", self._check_git, "secondary", width=140).pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            btn_row,
            text="Download Git",
            command=self._open_git_download,
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color="transparent",
            text_color=COLORS["accent"],
            hover_color=COLORS["bg_hover"],
            corner_radius=8,
            width=120,
            height=36,
        ).pack(side="left")

    def _build_install_step(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(
            card,
            text="Step 3 — Install Kometa",
            font=ctk.CTkFont("Segoe UI Semibold", 14),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=20, pady=(16, 8))

        ctk.CTkLabel(
            card,
            text="Choose where to install Kometa. A folder will be created there with all required files.",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=20, pady=(0, 12))

        dir_row = ctk.CTkFrame(card, fg_color="transparent")
        dir_row.pack(anchor="w", padx=20, pady=(0, 8), fill="x")

        self._install_dir_entry = self.make_entry(dir_row, "C:\\Kometa", width=420)
        saved = self.config.get("kometa_install_dir")
        if saved:
            self._install_dir_entry.insert(0, saved)
        self._install_dir_entry.pack(side="left", padx=(0, 10))
        self.make_button(dir_row, "Browse", self._browse_install_dir, "secondary", width=80).pack(side="left")

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(anchor="w", padx=20, pady=(0, 16))
        self.make_button(btn_row, "Install Kometa", self._start_install, "primary", width=160).pack(side="left")

        self._install_status = ctk.CTkLabel(
            btn_row,
            text="",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        )
        self._install_status.pack(side="left", padx=12)

    def _build_update_section(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(
            card,
            text="Update Kometa",
            font=ctk.CTkFont("Segoe UI Semibold", 14),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=20, pady=(16, 8))

        info_row = ctk.CTkFrame(card, fg_color="transparent")
        info_row.pack(anchor="w", padx=20, pady=(0, 8), fill="x")

        self._installed_ver_label = ctk.CTkLabel(
            info_row,
            text="Installed: —",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        )
        self._installed_ver_label.pack(side="left", padx=(0, 20))

        self._latest_ver_label = ctk.CTkLabel(
            info_row,
            text="Latest: —",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        )
        self._latest_ver_label.pack(side="left")

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(anchor="w", padx=20, pady=(0, 16))
        self.make_button(btn_row, "Check for Updates", self._check_version, "secondary", width=160).pack(side="left", padx=(0, 10))
        self.make_button(btn_row, "Update Now", self._start_update, "primary", width=120).pack(side="left")

    def _build_log_area(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(
            card,
            text="Output",
            font=ctk.CTkFont("Segoe UI Semibold", 13),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=20, pady=(14, 6))

        self._log_box = ctk.CTkTextbox(
            card,
            height=180,
            font=ctk.CTkFont("Consolas", 11),
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_primary"],
            border_width=0,
            state="disabled",
        )
        self._log_box.pack(fill="x", padx=20, pady=(0, 16))

    # ── Actions ───────────────────────────────────────────────────────────────

    def _log(self, msg: str):
        def _do():
            self._log_box.configure(state="normal")
            self._log_box.insert("end", msg + "\n")
            self._log_box.see("end")
            self._log_box.configure(state="disabled")
        self.after(0, _do)

    def _check_python(self):
        python = self.kometa.detect_python()
        if python:
            self._python_badge.configure(text=" Found ✓ ", text_color=COLORS["accent_green"], fg_color=COLORS["accent_green"] + "22")
            self._python_detail.configure(text=f"Python found at: {python}")
            self.config.set("python_path", python)
        else:
            self._python_badge.configure(text=" Not Found ", text_color=COLORS["accent_red"], fg_color=COLORS["accent_red"] + "22")
            self._python_detail.configure(text="Python 3.10+ not found. Please install it and try again.")

    def _check_git(self):
        if self.kometa.is_git_available():
            self._git_badge.configure(text=" Found ✓ ", text_color=COLORS["accent_green"], fg_color=COLORS["accent_green"] + "22")
            self._git_detail.configure(text="Git is available.")
        else:
            self._git_badge.configure(text=" Not Found ", text_color=COLORS["accent_red"], fg_color=COLORS["accent_red"] + "22")
            self._git_detail.configure(text="Git not found. Download and install Git for Windows.")

    def _open_python_download(self):
        import webbrowser
        webbrowser.open("https://www.python.org/downloads/windows/")

    def _open_git_download(self):
        import webbrowser
        webbrowser.open("https://git-scm.com/download/win")

    def _browse_install_dir(self):
        path = fd.askdirectory(title="Choose Kometa Install Directory")
        if path:
            self._install_dir_entry.delete(0, "end")
            self._install_dir_entry.insert(0, path)

    def _start_install(self):
        install_dir = self._install_dir_entry.get().strip()
        if not install_dir:
            self._install_status.configure(text="Please enter an install directory", text_color=COLORS["accent_yellow"])
            return

        self._install_status.configure(text="Installing...", text_color=COLORS["text_secondary"])

        def _run():
            success = self.kometa.install_kometa(install_dir, progress_callback=self._log)
            def _done():
                if success:
                    self._install_status.configure(text="✓ Installed!", text_color=COLORS["accent_green"])
                else:
                    self._install_status.configure(text="✗ Installation failed", text_color=COLORS["accent_red"])
            self.after(0, _done)

        threading.Thread(target=_run, daemon=True).start()

    def _check_version(self):
        installed = self.kometa.get_installed_version()
        self._installed_ver_label.configure(text=f"Installed: {installed or '—'}")

        def _fetch():
            latest = self.kometa.get_latest_version()
            self.after(0, lambda: self._latest_ver_label.configure(
                text=f"Latest: {latest or '—'}"
            ))
        threading.Thread(target=_fetch, daemon=True).start()

    def _start_update(self):
        def _run():
            self._log("Starting update...")
            self.kometa.update_kometa(progress_callback=self._log)
        threading.Thread(target=_run, daemon=True).start()

    def on_show(self):
        self._check_python()
        self._check_git()
        installed = self.kometa.get_installed_version()
        self._installed_ver_label.configure(text=f"Installed: {installed or '—'}")
