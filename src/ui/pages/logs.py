"""
LogsPage - Browse and search Kometa run logs
"""

import customtkinter as ctk
from pathlib import Path
from src.ui.pages.base_page import BasePage
from src.ui.theme import COLORS


class LogsPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_log = None
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=32, pady=(24, 16))
        top.grid_columnconfigure(1, weight=1)

        self.make_page_header(top, "Logs", "Browse and search Kometa run logs").grid(row=0, column=0, sticky="w")

        search_row = ctk.CTkFrame(top, fg_color="transparent")
        search_row.grid(row=0, column=1, sticky="e")

        self._search_entry = self.make_entry(search_row, "Search logs...", width=280)
        self._search_entry.pack(side="left", padx=(0, 8))
        self._search_entry.bind("<Return>", lambda e: self._do_search())
        self.make_button(search_row, "Search", self._do_search, "secondary", width=80).pack(side="left", padx=(0, 8))
        self.make_button(search_row, "Errors Only", lambda: self._filter("ERROR"), "danger", width=100).pack(side="left")

        # Split: file list + log viewer
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 24))
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # File list
        file_panel = ctk.CTkFrame(
            main, width=240, fg_color=COLORS["bg_card"], corner_radius=12, border_width=1, border_color=COLORS["border"]
        )
        file_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        file_panel.grid_propagate(False)

        ctk.CTkLabel(file_panel, text="Log Files", font=ctk.CTkFont("Segoe UI Semibold", 13), text_color=COLORS["text_secondary"]).pack(anchor="w", padx=12, pady=(12, 6))

        self._file_list = ctk.CTkScrollableFrame(file_panel, fg_color="transparent")
        self._file_list.pack(fill="both", expand=True, padx=4, pady=(0, 8))

        # Log viewer
        log_panel = ctk.CTkFrame(main, fg_color=COLORS["bg_card"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        log_panel.grid(row=0, column=1, sticky="nsew")
        log_panel.grid_rowconfigure(1, weight=1)
        log_panel.grid_columnconfigure(0, weight=1)

        self._log_file_label = ctk.CTkLabel(
            log_panel, text="Select a log file", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_muted"]
        )
        self._log_file_label.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))

        self._log_viewer = ctk.CTkTextbox(
            log_panel, font=ctk.CTkFont("Consolas", 10), fg_color=COLORS["bg_input"],
            text_color=COLORS["text_primary"], border_width=0, corner_radius=0, state="disabled", wrap="none"
        )
        self._log_viewer.grid(row=1, column=0, sticky="nsew", padx=1, pady=(0, 1))

    def _get_log_files(self) -> list[Path]:
        cfg_dir = self.config.get("kometa_config_dir")
        if not cfg_dir:
            return []
        logs_dir = Path(cfg_dir) / "logs"
        if not logs_dir.exists():
            return []
        return sorted(logs_dir.glob("*.log"), reverse=True)

    def _refresh_file_list(self):
        for w in self._file_list.winfo_children():
            w.destroy()
        files = self._get_log_files()
        if not files:
            ctk.CTkLabel(self._file_list, text="No logs found", font=ctk.CTkFont("Segoe UI", 11), text_color=COLORS["text_muted"]).pack(pady=12)
            return
        for f in files:
            btn = ctk.CTkButton(
                self._file_list, text=f.name, anchor="w",
                command=lambda p=f: self._open_log(p),
                font=ctk.CTkFont("Consolas", 10),
                fg_color="transparent", text_color=COLORS["text_secondary"],
                hover_color=COLORS["bg_hover"], corner_radius=6, height=30,
            )
            btn.pack(fill="x", pady=1)

    def _open_log(self, path: Path):
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            self._current_log = content
            self._show_content(content)
            self._log_file_label.configure(text=path.name, text_color=COLORS["text_primary"])
        except Exception as e:
            self._show_content(f"Error reading log: {e}")

    def _show_content(self, content: str):
        self._log_viewer.configure(state="normal")
        self._log_viewer.delete("1.0", "end")
        self._log_viewer.insert("1.0", content)
        self._log_viewer.configure(state="disabled")

    def _do_search(self):
        if not self._current_log:
            return
        term = self._search_entry.get().strip().lower()
        if not term:
            self._show_content(self._current_log)
            return
        filtered = "\n".join(line for line in self._current_log.splitlines() if term in line.lower())
        self._show_content(filtered or "No matches found.")

    def _filter(self, level: str):
        if not self._current_log:
            return
        filtered = "\n".join(line for line in self._current_log.splitlines() if level in line)
        self._show_content(filtered or f"No {level} entries found.")

    def on_show(self):
        self._refresh_file_list()
