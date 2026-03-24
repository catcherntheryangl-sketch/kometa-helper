"""
Kometa Helper - Windows GUI for Kometa (Plex Metadata Manager)
Entry point
"""

import sys
import os

# Ensure the src directory is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.app import KometaHelperApp

if __name__ == "__main__":
    app = KometaHelperApp()
    app.run()
