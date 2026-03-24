"""
ConfigManager - Handles all application state, settings, and Kometa YAML files
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
import yaml


APP_DATA_DIR = Path(os.getenv("APPDATA", Path.home())) / "KometaHelper"
SETTINGS_FILE = APP_DATA_DIR / "settings.json"
BACKUP_DIR = APP_DATA_DIR / "backups"

DEFAULT_SETTINGS = {
    "kometa_install_dir": "",
    "kometa_config_dir": "",
    "python_path": "",
    "auto_update_check": True,
    "notification_on_complete": True,
    "notification_on_error": True,
    "theme": "dark",
    "accent": "blue",
    "scheduled_runs": [],
    "last_run": None,
    "plex_url": "",
    "plex_token": "",
    "tmdb_api_key": "",
    "trakt_client_id": "",
    "trakt_client_secret": "",
    "mdblist_api_key": "",
    "radarr_url": "",
    "radarr_api_key": "",
    "sonarr_url": "",
    "sonarr_api_key": "",
    "onboarding_complete": False,
}


class ConfigManager:
    def __init__(self):
        APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        self.settings = self._load_settings()

    def _load_settings(self) -> dict:
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r") as f:
                    loaded = json.load(f)
                # Merge with defaults so new keys always exist
                merged = {**DEFAULT_SETTINGS, **loaded}
                return merged
            except Exception:
                pass
        return dict(DEFAULT_SETTINGS)

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f, indent=2, default=str)

    def get(self, key: str, default=None):
        return self.settings.get(key, default)

    def set(self, key: str, value):
        self.settings[key] = value
        self.save_settings()

    def get_kometa_config_path(self) -> Path | None:
        cfg_dir = self.get("kometa_config_dir")
        if cfg_dir:
            p = Path(cfg_dir) / "config.yml"
            if p.exists():
                return p
        return None

    def load_kometa_config(self) -> dict:
        path = self.get_kometa_config_path()
        if path and path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    def save_kometa_config(self, data: dict, backup: bool = True):
        path = self.get_kometa_config_path()
        if not path:
            cfg_dir = self.get("kometa_config_dir")
            if not cfg_dir:
                raise ValueError("No Kometa config directory set")
            path = Path(cfg_dir) / "config.yml"

        if backup and path.exists():
            self._backup_file(path)

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def _backup_file(self, path: Path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{path.stem}_{timestamp}{path.suffix}"
        shutil.copy2(path, BACKUP_DIR / backup_name)
        # Keep only the last 20 backups
        backups = sorted(BACKUP_DIR.glob(f"{path.stem}_*"))
        for old in backups[:-20]:
            old.unlink()

    def get_collection_files(self) -> list[Path]:
        cfg_dir = self.get("kometa_config_dir")
        if not cfg_dir:
            return []
        p = Path(cfg_dir)
        return sorted(p.glob("*.yml")) + sorted((p / "collections").glob("*.yml")) if (p / "collections").exists() else sorted(p.glob("*.yml"))

    def load_yaml_file(self, path: Path) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def save_yaml_file(self, path: Path, data: dict, backup: bool = True):
        if backup and path.exists():
            self._backup_file(path)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def validate_yaml_string(self, yaml_str: str) -> tuple[bool, str]:
        """Returns (is_valid, error_message)"""
        try:
            yaml.safe_load(yaml_str)
            return True, ""
        except yaml.YAMLError as e:
            return False, str(e)

    def get_backups(self) -> list[Path]:
        return sorted(BACKUP_DIR.glob("*.yml"), reverse=True)
