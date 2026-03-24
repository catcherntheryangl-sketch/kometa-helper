"""
RunnerPage - Run Kometa with configurable flags and live output
"""

import customtkinter as ctk
from datetime import datetime
from src.ui.pages.base_page import BasePage
from src.ui.theme import COLORS

LOG_COLORS = {
    "INFO":    "#e6edf3",
    "WARNING": "#d29922",
    "ERROR":   "#f85149",
    "SUCCESS": "#3fb950",
}

RUN_FLAGS = [
    ("--run",             "Run immediately (skip scheduled times)", True),
    ("--run-collections", "Run collections only",                  False),
    ("--run-overlays",    "Run overlays only",                     False),
    ("--run-operations",  "Run operations only",                   False),
    ("--collections-only","Collections only (alias)",              False),
    ("--overlays-only",   "Overlays only (alias)",                 False),
    ("--operations-only", "Operations only (alias)",               False),
    ("--delete-collections","Delete managed collections",          False),
    ("--resume COLLECTION","Resume from a specific collection",    False),
    ("--no-countdown",    "Skip the startup countdown",            True),
    ("--ignore-schedules","Ignore scheduled run times",            False),
    ("--debug",           "Enable verbose debug logging",          False),
    ("--trace",           "Enable trace logging (very verbose)",   False),
]


class RunnerPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._flag_vars = {}
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top section
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=32, pady=(24, 16))
        top.grid_columnconfigure(1, weight=1)

        self.make_page_header(top, "Run Kometa", "Start a Kometa run with your chosen options").grid(row=0, column=0, sticky="w")

        control_row = ctk.CTkFrame(top, fg_color="transparent")
        control_row.grid(row=0, column=1, sticky="e")

        self._run_btn = self.make_button(control_row, "▶  Run Kometa", self._start_run, "success", width=150)
        self._run_btn.pack(side="left", padx=(0, 10))

        self._stop_btn = self.make_button(control_row, "⏹  Stop", self._stop_run, "danger", width=100)
        self._stop_btn.pack(side="left")
        self._stop_btn.configure(state="disabled")

        # Main content: flags left, log right
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 24))
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Left: flags panel
        flags_panel = ctk.CTkFrame(
            main,
            width=300,
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        flags_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        flags_panel.grid_propagate(False)

        ctk.CTkLabel(
            flags_panel,
            text="Run Flags",
            font=ctk.CTkFont("Segoe UI Semibold", 14),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=16, pady=(16, 4))

        ctk.CTkLabel(
            flags_panel,
            text="Command preview:",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=16, pady=(0, 4))

        self._cmd_preview = ctk.CTkLabel(
            flags_panel,
            text="python kometa.py",
            font=ctk.CTkFont("Consolas", 10),
            text_color=COLORS["accent"],
            wraplength=260,
            justify="left",
            anchor="w",
        )
        self._cmd_preview.pack(anchor="w", padx=16, pady=(0, 12))

        ctk.CTkFrame(flags_panel, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=12, pady=(0, 8))

        flags_scroll = ctk.CTkScrollableFrame(flags_panel, fg_color="transparent")
        flags_scroll.pack(fill="both", expand=True, padx=0, pady=(0, 8))

        for flag, description, default in RUN_FLAGS:
            var = ctk.BooleanVar(value=default)
            self._flag_vars[flag] = var
            frame = ctk.CTkFrame(flags_scroll, fg_color="transparent")
            frame.pack(fill="x", padx=12, pady=2)
            cb = ctk.CTkCheckBox(
                frame,
                text=flag.split(" ")[0],
                variable=var,
                command=self._update_cmd_preview,
                font=ctk.CTkFont("Consolas", 11),
                text_color=COLORS["text_primary"],
                fg_color=COLORS["accent"],
                hover_color=COLORS["accent_dim"],
                checkmark_color="#000000",
                border_color=COLORS["border"],
            )
            cb.pack(anchor="w")
            ctk.CTkLabel(
                frame,
                text=description,
                font=ctk.CTkFont("Segoe UI", 10),
                text_color=COLORS["text_muted"],
            ).pack(anchor="w", padx=24)

        # Right: log panel
        log_panel = ctk.CTkFrame(
            main,
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        log_panel.grid(row=0, column=1, sticky="nsew")
        log_panel.grid_rowconfigure(1, weight=1)
        log_panel.grid_columnconfigure(0, weight=1)

        log_header = ctk.CTkFrame(log_panel, fg_color="transparent", height=44)
        log_header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 0))

        ctk.CTkLabel(
            log_header,
            text="Live Output",
            font=ctk.CTkFont("Segoe UI Semibold", 13),
            text_color=COLORS["text_secondary"],
        ).pack(side="left")

        ctk.CTkButton(
            log_header,
            text="Clear",
            command=self._clear_log,
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color="transparent",
            text_color=COLORS["text_secondary"],
            hover_color=COLORS["bg_hover"],
            width=60,
            height=28,
            corner_radius=6,
        ).pack(side="right")

        self._status_badge = ctk.CTkLabel(
            log_header,
            text=" Idle ",
            font=ctk.CTkFont("Segoe UI Semibold", 10),
            text_color=COLORS["text_muted"],
            fg_color=COLORS["bg_input"],
            corner_radius=4,
        )
        self._status_badge.pack(side="right", padx=(0, 8))

        self._log_box = ctk.CTkTextbox(
            log_panel,
            font=ctk.CTkFont("Consolas", 11),
            fg_color=COLORS["bg_input"],
            text_color=COLORS["text_primary"],
            border_width=0,
            corner_radius=0,
            state="disabled",
            wrap="none",
        )
        self._log_box.grid(row=1, column=0, sticky="nsew", padx=1, pady=(4, 1))

        self._update_cmd_preview()

    def _update_cmd_preview(self):
        flags = [f.split(" ")[0] for f, var in self._flag_vars.items() if var.get()]
        cmd = "python kometa.py " + " ".join(flags)
        self._cmd_preview.configure(text=cmd.strip())

    def _start_run(self):
        flags = [f.split(" ")[0] for f, var in self._flag_vars.items() if var.get()]

        self._run_btn.configure(state="disabled")
        self._stop_btn.configure(state="normal")
        self._set_status("running", COLORS["accent_green"])
        self._log_line(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Kometa...", "INFO")

        self.kometa.run_kometa(
            flags=flags,
            log_callback=self._on_log,
            done_callback=self._on_done,
        )

    def _stop_run(self):
        self.kometa.stop_kometa()
        self._log_line("⏹ Run stopped by user", "WARNING")
        self._set_status("stopped", COLORS["accent_red"])
        self._run_btn.configure(state="normal")
        self._stop_btn.configure(state="disabled")

    def _on_log(self, message: str, level: str):
        self.after(0, lambda m=message, l=level: self._log_line(m, l))

    def _on_done(self, exit_code: int):
        def _finish():
            self._run_btn.configure(state="normal")
            self._stop_btn.configure(state="disabled")
            if exit_code == 0:
                self._set_status("done", COLORS["accent_green"])
                self._log_line(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Kometa finished (exit code 0)", "SUCCESS")
            else:
                self._set_status("error", COLORS["accent_red"])
                self._log_line(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Kometa exited with code {exit_code}", "ERROR")
            from datetime import datetime as dt
            self.config.set("last_run", dt.now().isoformat())
        self.after(0, _finish)

    def _log_line(self, message: str, level: str = "INFO"):
        color = LOG_COLORS.get(level, LOG_COLORS["INFO"])
        self._log_box.configure(state="normal")
        self._log_box.insert("end", message + "\n")
        self._log_box.see("end")
        self._log_box.configure(state="disabled")

    def _clear_log(self):
        self._log_box.configure(state="normal")
        self._log_box.delete("1.0", "end")
        self._log_box.configure(state="disabled")

    def _set_status(self, label: str, color: str):
        text_map = {
            "running": " Running ",
            "stopped": " Stopped ",
            "done":    " Done ✓ ",
            "error":   " Error ✗ ",
            "idle":    " Idle ",
        }
        self._status_badge.configure(
            text=text_map.get(label, f" {label} "),
            text_color=color,
            fg_color=color + "22",
        )
