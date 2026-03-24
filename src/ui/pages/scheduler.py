"""
SchedulerPage - Visual Windows Task Scheduler integration for Kometa
"""

import json
import subprocess
import customtkinter as ctk
from src.ui.pages.base_page import BasePage
from src.ui.theme import COLORS

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
RUN_TYPES = ["Full Run", "Collections Only", "Overlays Only", "Operations Only"]

FLAG_MAP = {
    "Full Run":          ["--run", "--no-countdown"],
    "Collections Only":  ["--run", "--no-countdown", "--collections-only"],
    "Overlays Only":     ["--run", "--no-countdown", "--overlays-only"],
    "Operations Only":   ["--run", "--no-countdown", "--operations-only"],
}


class SchedulerPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=32, pady=24)
        scroll.grid_columnconfigure(0, weight=1)

        self.make_page_header(
            scroll, "Scheduler", "Automate Kometa with Windows Task Scheduler"
        ).grid(row=0, column=0, sticky="w", pady=(0, 24))

        # Info card
        info = self.make_card(scroll)
        info.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        ctk.CTkLabel(
            info,
            text="ℹ  Kometa Helper can create Windows Task Scheduler entries to run Kometa automatically.\n"
                 "Tasks run silently in the background even when you're not logged in (if configured).",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
            justify="left",
            wraplength=750,
        ).pack(anchor="w", padx=20, pady=14)

        # New task builder
        self._build_new_task(scroll, row=2)

        # Existing tasks
        self._build_task_list(scroll, row=3)

    def _build_new_task(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 20))

        self.make_section_label(card, "Create New Scheduled Task").pack(anchor="w", padx=20, pady=(16, 12))

        # Task name
        row1 = ctk.CTkFrame(card, fg_color="transparent")
        row1.pack(anchor="w", padx=20, pady=(0, 10), fill="x")
        ctk.CTkLabel(row1, text="Task Name", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"], width=120, anchor="w").pack(side="left")
        self._task_name = self.make_entry(row1, "KometaHelper_Daily", width=280)
        self._task_name.pack(side="left")

        # Run type
        row2 = ctk.CTkFrame(card, fg_color="transparent")
        row2.pack(anchor="w", padx=20, pady=(0, 10))
        ctk.CTkLabel(row2, text="Run Type", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"], width=120, anchor="w").pack(side="left")
        self._run_type = ctk.CTkOptionMenu(
            row2,
            values=RUN_TYPES,
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color=COLORS["bg_input"],
            button_color=COLORS["bg_hover"],
            text_color=COLORS["text_primary"],
            dropdown_fg_color=COLORS["bg_card"],
            width=200,
        )
        self._run_type.pack(side="left")

        # Time
        row3 = ctk.CTkFrame(card, fg_color="transparent")
        row3.pack(anchor="w", padx=20, pady=(0, 10))
        ctk.CTkLabel(row3, text="Time (24h)", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"], width=120, anchor="w").pack(side="left")
        self._run_hour = ctk.CTkOptionMenu(
            row3,
            values=[str(i).zfill(2) for i in range(24)],
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color=COLORS["bg_input"],
            button_color=COLORS["bg_hover"],
            text_color=COLORS["text_primary"],
            dropdown_fg_color=COLORS["bg_card"],
            width=80,
        )
        self._run_hour.set("02")
        self._run_hour.pack(side="left", padx=(0, 6))

        ctk.CTkLabel(row3, text=":", font=ctk.CTkFont("Segoe UI Semibold", 14), text_color=COLORS["text_secondary"]).pack(side="left", padx=(0, 6))

        self._run_minute = ctk.CTkOptionMenu(
            row3,
            values=["00", "15", "30", "45"],
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color=COLORS["bg_input"],
            button_color=COLORS["bg_hover"],
            text_color=COLORS["text_primary"],
            dropdown_fg_color=COLORS["bg_card"],
            width=80,
        )
        self._run_minute.set("00")
        self._run_minute.pack(side="left")

        # Days
        row4 = ctk.CTkFrame(card, fg_color="transparent")
        row4.pack(anchor="w", padx=20, pady=(0, 12))
        ctk.CTkLabel(row4, text="Days", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"], width=120, anchor="w").pack(side="left")

        self._day_vars = {}
        days_frame = ctk.CTkFrame(row4, fg_color="transparent")
        days_frame.pack(side="left")
        for day in DAYS:
            var = ctk.BooleanVar(value=True)
            self._day_vars[day] = var
            ctk.CTkCheckBox(
                days_frame,
                text=day[:3],
                variable=var,
                font=ctk.CTkFont("Segoe UI", 11),
                text_color=COLORS["text_primary"],
                fg_color=COLORS["accent"],
                hover_color=COLORS["accent_dim"],
                checkmark_color="#000000",
                border_color=COLORS["border"],
                width=64,
            ).pack(side="left", padx=(0, 4))

        # Create button
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(anchor="w", padx=20, pady=(0, 16))
        self.make_button(btn_row, "Create Task", self._create_task, "primary", width=140).pack(side="left", padx=(0, 12))
        self._task_status = ctk.CTkLabel(btn_row, text="", font=ctk.CTkFont("Segoe UI", 12), text_color=COLORS["text_secondary"])
        self._task_status.pack(side="left")

    def _build_task_list(self, parent, row):
        card = self.make_card(parent)
        card.grid(row=row, column=0, sticky="ew")

        header_row = ctk.CTkFrame(card, fg_color="transparent")
        header_row.pack(fill="x", padx=20, pady=(16, 8))
        self.make_section_label(header_row, "Existing Kometa Tasks").pack(side="left")
        self.make_button(header_row, "Refresh", self._refresh_tasks, "secondary", width=90).pack(side="right")

        self._task_list_frame = ctk.CTkFrame(card, fg_color="transparent")
        self._task_list_frame.pack(fill="x", padx=20, pady=(0, 16))
        self._refresh_tasks()

    def _create_task(self):
        import platform
        if platform.system() != "Windows":
            self._task_status.configure(text="Task Scheduler is Windows-only", text_color=COLORS["accent_yellow"])
            return

        name = self._task_name.get().strip()
        run_type = self._run_type.get()
        hour = self._run_hour.get()
        minute = self._run_minute.get()
        days = [d for d, v in self._day_vars.items() if v.get()]

        if not name:
            self._task_status.configure(text="Enter a task name", text_color=COLORS["accent_yellow"])
            return
        if not days:
            self._task_status.configure(text="Select at least one day", text_color=COLORS["accent_yellow"])
            return

        install_dir = self.config.get("kometa_install_dir")
        config_path = self.config.get_kometa_config_path()
        python_venv = ""
        if install_dir:
            import os
            venv_python = os.path.join(install_dir, "venv", "Scripts", "python.exe")
            if os.path.exists(venv_python):
                python_venv = venv_python

        python_cmd = python_venv or self.config.get("python_path") or "python"
        kometa_script = os.path.join(install_dir, "kometa.py") if install_dir else "kometa.py"
        flags = FLAG_MAP.get(run_type, ["--run"])
        if config_path:
            flags += ["--config", str(config_path)]

        action = f'"{python_cmd}" "{kometa_script}" {" ".join(flags)}'
        days_str = ",".join(d.upper()[:3] for d in days)

        # Build schtasks command
        cmd = [
            "schtasks", "/create",
            "/tn", name,
            "/tr", action,
            "/sc", "WEEKLY",
            "/d", days_str,
            "/st", f"{hour}:{minute}",
            "/f",  # force overwrite
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                self._task_status.configure(text="✓ Task created!", text_color=COLORS["accent_green"])
                self._save_task_record(name, run_type, hour, minute, days)
                self._refresh_tasks()
            else:
                self._task_status.configure(text=f"Error: {result.stderr[:80]}", text_color=COLORS["accent_red"])
        except Exception as e:
            self._task_status.configure(text=f"Error: {e}", text_color=COLORS["accent_red"])

    def _save_task_record(self, name, run_type, hour, minute, days):
        tasks = self.config.get("scheduled_runs", [])
        # Remove existing with same name
        tasks = [t for t in tasks if t.get("name") != name]
        tasks.append({
            "name": name,
            "run_type": run_type,
            "time": f"{hour}:{minute}",
            "days": days,
        })
        self.config.set("scheduled_runs", tasks)

    def _refresh_tasks(self):
        for w in self._task_list_frame.winfo_children():
            w.destroy()

        tasks = self.config.get("scheduled_runs", [])
        if not tasks:
            ctk.CTkLabel(
                self._task_list_frame,
                text="No scheduled tasks yet.",
                font=ctk.CTkFont("Segoe UI", 12),
                text_color=COLORS["text_muted"],
            ).pack(pady=16)
            return

        for task in tasks:
            row = ctk.CTkFrame(self._task_list_frame, fg_color=COLORS["bg_input"], corner_radius=8)
            row.pack(fill="x", pady=4)

            ctk.CTkLabel(
                row,
                text=f"📅  {task['name']}",
                font=ctk.CTkFont("Segoe UI Semibold", 12),
                text_color=COLORS["text_primary"],
            ).pack(side="left", padx=12, pady=10)

            days_str = ", ".join(task.get("days", []))
            ctk.CTkLabel(
                row,
                text=f"{task.get('run_type', '?')}  ·  {task.get('time', '?')}  ·  {days_str}",
                font=ctk.CTkFont("Segoe UI", 11),
                text_color=COLORS["text_secondary"],
            ).pack(side="left", padx=(0, 12))

            ctk.CTkButton(
                row,
                text="Delete",
                command=lambda n=task["name"]: self._delete_task(n),
                font=ctk.CTkFont("Segoe UI", 11),
                fg_color="transparent",
                text_color=COLORS["accent_red"],
                hover_color=COLORS["accent_red"] + "22",
                corner_radius=6,
                width=70,
                height=28,
            ).pack(side="right", padx=12)

    def _delete_task(self, name: str):
        import platform
        if platform.system() == "Windows":
            try:
                subprocess.run(["schtasks", "/delete", "/tn", name, "/f"], capture_output=True)
            except Exception:
                pass
        tasks = [t for t in self.config.get("scheduled_runs", []) if t.get("name") != name]
        self.config.set("scheduled_runs", tasks)
        self._refresh_tasks()
