"""
KometaManager - Installs, runs, updates, and monitors Kometa
"""

import os
import sys
import subprocess
import threading
import shutil
import platform
from pathlib import Path
from typing import Callable, Optional
import requests

KOMETA_REPO = "https://api.github.com/repos/Kometa-Team/Kometa/releases/latest"
KOMETA_CLONE_URL = "https://github.com/Kometa-Team/Kometa.git"
PYTHON_DOWNLOAD_URL = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"


class KometaManager:
    def __init__(self, config_manager):
        self.config = config_manager
        self._process: Optional[subprocess.Popen] = None
        self._run_thread: Optional[threading.Thread] = None
        self.on_log: Optional[Callable[[str, str], None]] = None  # (message, level)
        self.on_status_change: Optional[Callable[[str], None]] = None
        self._running = False

    # ── Installation ──────────────────────────────────────────────────────────

    def detect_python(self) -> Optional[str]:
        """Try to find a usable Python 3.10+ executable."""
        candidates = ["python", "python3", "py"]
        for cmd in candidates:
            try:
                result = subprocess.run(
                    [cmd, "--version"], capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    version_str = result.stdout.strip() or result.stderr.strip()
                    parts = version_str.split()
                    if len(parts) >= 2:
                        ver = tuple(int(x) for x in parts[1].split(".")[:2])
                        if ver >= (3, 10):
                            return cmd
            except Exception:
                pass
        return None

    def is_git_available(self) -> bool:
        try:
            subprocess.run(["git", "--version"], capture_output=True, timeout=5)
            return True
        except Exception:
            return False

    def is_kometa_installed(self) -> bool:
        install_dir = self.config.get("kometa_install_dir")
        if not install_dir:
            return False
        kometa_py = Path(install_dir) / "kometa.py"
        return kometa_py.exists()

    def install_kometa(
        self, install_dir: str, progress_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """Clone Kometa into install_dir and set up a venv."""
        try:
            install_path = Path(install_dir)
            install_path.mkdir(parents=True, exist_ok=True)

            def log(msg):
                if progress_callback:
                    progress_callback(msg)
                self._log(msg, "INFO")

            log("Cloning Kometa from GitHub...")
            result = subprocess.run(
                ["git", "clone", KOMETA_CLONE_URL, str(install_path)],
                capture_output=True, text=True, timeout=120,
            )
            if result.returncode != 0:
                log(f"Git clone failed: {result.stderr}")
                return False

            log("Creating Python virtual environment...")
            python_cmd = self.config.get("python_path") or self.detect_python() or "python"
            result = subprocess.run(
                [python_cmd, "-m", "venv", str(install_path / "venv")],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode != 0:
                log(f"Venv creation failed: {result.stderr}")
                return False

            log("Installing Kometa dependencies...")
            pip_path = (
                install_path / "venv" / ("Scripts" if platform.system() == "Windows" else "bin") / "pip"
            )
            result = subprocess.run(
                [str(pip_path), "install", "-r", str(install_path / "requirements.txt")],
                capture_output=True, text=True, timeout=300,
            )
            if result.returncode != 0:
                log(f"Pip install failed: {result.stderr}")
                return False

            self.config.set("kometa_install_dir", str(install_path))
            if not self.config.get("kometa_config_dir"):
                config_dir = install_path / "config"
                config_dir.mkdir(exist_ok=True)
                self.config.set("kometa_config_dir", str(config_dir))

            log("✓ Kometa installed successfully!")
            return True

        except Exception as e:
            if progress_callback:
                progress_callback(f"Installation error: {e}")
            return False

    def update_kometa(self, progress_callback: Optional[Callable[[str], None]] = None) -> bool:
        install_dir = self.config.get("kometa_install_dir")
        if not install_dir:
            return False
        try:
            def log(msg):
                if progress_callback:
                    progress_callback(msg)
                self._log(msg, "INFO")

            log("Pulling latest changes from GitHub...")
            result = subprocess.run(
                ["git", "pull"],
                capture_output=True, text=True, timeout=120,
                cwd=install_dir,
            )
            if result.returncode != 0:
                log(f"Git pull failed: {result.stderr}")
                return False
            log("✓ Kometa updated successfully!")
            return True
        except Exception as e:
            if progress_callback:
                progress_callback(f"Update error: {e}")
            return False

    def get_installed_version(self) -> Optional[str]:
        install_dir = self.config.get("kometa_install_dir")
        if not install_dir:
            return None
        version_file = Path(install_dir) / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        return None

    def get_latest_version(self) -> Optional[str]:
        try:
            r = requests.get(KOMETA_REPO, timeout=10)
            if r.status_code == 200:
                return r.json().get("tag_name", "").lstrip("v")
        except Exception:
            pass
        return None

    # ── Running ───────────────────────────────────────────────────────────────

    def is_running(self) -> bool:
        return self._running and self._process is not None and self._process.poll() is None

    def run_kometa(
        self,
        flags: list[str] = None,
        log_callback: Optional[Callable[[str, str], None]] = None,
        done_callback: Optional[Callable[[int], None]] = None,
    ):
        """Start Kometa in a background thread, streaming output."""
        if self.is_running():
            self._log("Kometa is already running", "WARNING")
            return

        install_dir = self.config.get("kometa_install_dir")
        if not install_dir:
            self._log("Kometa not installed", "ERROR")
            return

        install_path = Path(install_dir)
        python_venv = install_path / "venv" / ("Scripts" if platform.system() == "Windows" else "bin") / "python"
        python_cmd = str(python_venv) if python_venv.exists() else (self.config.get("python_path") or "python")
        kometa_script = install_path / "kometa.py"
        config_path = self.config.get_kometa_config_path()

        cmd = [python_cmd, str(kometa_script)]
        if config_path:
            cmd += ["--config", str(config_path)]
        if flags:
            cmd += flags

        def _stream():
            self._running = True
            if self.on_status_change:
                self.on_status_change("running")
            try:
                self._process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    cwd=str(install_path),
                )
                for line in self._process.stdout:
                    line = line.rstrip()
                    level = "INFO"
                    if "ERROR" in line.upper():
                        level = "ERROR"
                    elif "WARNING" in line.upper() or "WARN" in line.upper():
                        level = "WARNING"
                    elif "SUCCESS" in line.upper() or "✓" in line:
                        level = "SUCCESS"
                    if log_callback:
                        log_callback(line, level)
                    self._log(line, level)

                self._process.wait()
                exit_code = self._process.returncode
            except Exception as e:
                exit_code = -1
                self._log(f"Run error: {e}", "ERROR")
            finally:
                self._running = False
                if self.on_status_change:
                    self.on_status_change("idle")
                if done_callback:
                    done_callback(exit_code)

        self._run_thread = threading.Thread(target=_stream, daemon=True)
        self._run_thread.start()

    def stop_kometa(self):
        if self._process and self._process.poll() is None:
            self._process.terminate()
            self._log("Kometa process terminated", "WARNING")
            self._running = False

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _log(self, message: str, level: str = "INFO"):
        if self.on_log:
            self.on_log(message, level)

    def test_plex_connection(self, url: str, token: str) -> tuple[bool, str]:
        try:
            r = requests.get(
                f"{url.rstrip('/')}/identity",
                headers={"X-Plex-Token": token},
                timeout=8,
            )
            if r.status_code == 200:
                return True, "Connected successfully"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)

    def test_tmdb_connection(self, api_key: str) -> tuple[bool, str]:
        try:
            r = requests.get(
                f"https://api.themoviedb.org/3/configuration?api_key={api_key}",
                timeout=8,
            )
            if r.status_code == 200:
                return True, "Connected successfully"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)

    def test_mdblist_connection(self, api_key: str) -> tuple[bool, str]:
        try:
            r = requests.get(
                f"https://mdblist.com/api/?apikey={api_key}&s=test",
                timeout=8,
            )
            if r.status_code == 200:
                return True, "Connected successfully"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)

    def get_plex_libraries(self, url: str, token: str) -> list[dict]:
        """Returns list of {title, type, key} dicts from Plex."""
        try:
            import xml.etree.ElementTree as ET
            r = requests.get(
                f"{url.rstrip('/')}/library/sections",
                headers={"X-Plex-Token": token, "Accept": "application/xml"},
                timeout=8,
            )
            if r.status_code != 200:
                return []
            root = ET.fromstring(r.text)
            libs = []
            for directory in root.findall(".//Directory"):
                libs.append({
                    "title": directory.get("title", ""),
                    "type": directory.get("type", ""),
                    "key": directory.get("key", ""),
                })
            return libs
        except Exception:
            return []
