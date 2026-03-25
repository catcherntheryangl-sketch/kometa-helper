"""
Constants and configuration for the Kometa Helper application.
All hex colors are 6-digits to ensure compatibility with Tkinter/CustomTkinter.
"""

# Application Metadata
APP_CONFIG = {
    "name": "Kometa Helper",
    "version": "1.0.9",
    "author": "CatcherInTheRyan",
    "github_url": "https://github.com/catcherntheryangl-sketch/kometa-helper"
}

# UI Colors (Light Mode, Dark Mode)
COLORS = {
    "bg_primary": ("#ffffff", "#1a1b1e"),
    "bg_secondary": ("#f8f9fa", "#25262b"),
    "bg_hover": ("#e9ecef", "#2c2e33"),
    
    "text_primary": ("#212529", "#c1c2c5"),
    "text_secondary": ("#495057", "#909296"),
    
    "accent": ("#228be6", "#228be6"),        # Blue
    "accent_success": ("#40c057", "#40c057"), # Green
    "accent_error": ("#fa5252", "#fa5252"),   # Red
    "accent_yellow": ("#d29922", "#d29922"),  # Fixed: No 8-digit hex
}

# Installation Paths (Default)
DEFAULT_PATHS = {
    "kometa_dir": "C:/Kometa",
    "config_dir": "C:/Kometa/config",
    "python_min_version": (3, 10)
}

# External Links
LINKS = {
    "python_download": "https://www.python.org/downloads/",
    "git_download": "https://git-scm.com/downloads",
    "kometa_docs": "https://kometa.wiki",
    "kometa_discord": "https://discord.gg/kometa"
}
