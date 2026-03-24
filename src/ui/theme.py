"""
Theme - Color palette and UI constants for Kometa Helper
"""

# === KOMETA-INSPIRED DARK THEME ===
COLORS = {
    # Backgrounds
    "bg_dark":      "#0d1117",   # near-black, main window
    "bg_panel":     "#161b22",   # sidebar / panels
    "bg_card":      "#1c2333",   # cards, frames
    "bg_input":     "#21262d",   # inputs, textboxes
    "bg_hover":     "#2d333b",   # hover state

    # Kometa brand colors
    "accent":       "#0bc8e0",   # cyan accent (Kometa brand)
    "accent_dim":   "#0a9ab0",   # dimmer accent for hover
    "accent_green": "#3fb950",   # success green
    "accent_red":   "#f85149",   # error red
    "accent_yellow":"#d29922",   # warning yellow
    "accent_purple":"#bc8cff",   # info purple

    # Text
    "text_primary":   "#e6edf3",
    "text_secondary": "#8b949e",
    "text_muted":     "#484f58",
    "text_accent":    "#0bc8e0",

    # Borders
    "border":       "#30363d",
    "border_active":"#0bc8e0",

    # Status
    "status_running":  "#3fb950",
    "status_stopped":  "#f85149",
    "status_idle":     "#8b949e",

    # Sidebar nav
    "nav_active_bg":   "#1c2333",
    "nav_hover_bg":    "#21262d",
}

FONTS = {
    "heading":    ("Segoe UI Semibold", 18),
    "subheading": ("Segoe UI Semibold", 14),
    "body":       ("Segoe UI", 12),
    "small":      ("Segoe UI", 10),
    "mono":       ("Consolas", 11),
    "mono_small": ("Consolas", 10),
    "nav":        ("Segoe UI Semibold", 12),
    "badge":      ("Segoe UI Semibold", 10),
    "title":      ("Segoe UI Light", 24),
}

PADDING = {
    "page":    (32, 28),
    "card":    (20, 16),
    "section": (16, 12),
    "tight":   (8, 6),
}

RADIUS = {
    "card":    12,
    "button":  8,
    "input":   6,
    "badge":   4,
}

NAV_ITEMS = [
    ("🏠", "Dashboard",    "dashboard"),
    ("⚙️", "Install",      "install"),
    ("🔌", "Connections",  "connections"),
    ("📋", "YAML Editor",  "yaml_editor"),
    ("🗂️", "Collections",  "collections"),
    ("▶️", "Run Kometa",   "runner"),
    ("📅", "Scheduler",    "scheduler"),
    ("📜", "Logs",         "logs"),
    ("💾", "Backups",      "backups"),
    ("⚙️", "Settings",     "settings"),
]
