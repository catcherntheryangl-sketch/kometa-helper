import sys
import multiprocessing
from src.app import KometaHelperApp

def main():
    """Main entry point for the application."""
    app = KometaHelperApp()
    sys.exit(app.run())

if __name__ == "__main__":
    # CRITICAL: Prevents the EXE from crashing/looping on Windows
    multiprocessing.freeze_support()
    main()
