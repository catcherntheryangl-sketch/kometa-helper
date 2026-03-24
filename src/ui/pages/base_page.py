"""
BasePage - Common base for all page frames
"""

import customtkinter as ctk
from src.ui.theme import COLORS, FONTS


class BasePage(ctk.CTkFrame):
    def __init__(self, parent, config_manager, kometa_manager, navigate, **kwargs):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color=COLORS["bg_dark"],
            **kwargs,
        )
        self.config = config_manager
        self.kometa = kometa_manager
        self.navigate = navigate
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def make_page_header(self, parent, title: str, subtitle: str = "") -> ctk.CTkFrame:
        header = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont("Segoe UI Semibold", 22),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(
                header,
                text=subtitle,
                font=ctk.CTkFont("Segoe UI", 12),
                text_color=COLORS["text_secondary"],
            ).pack(anchor="w", pady=(2, 0))
        return header

    def make_card(self, parent, **kwargs) -> ctk.CTkFrame:
        defaults = dict(
            corner_radius=12,
            fg_color=COLORS["bg_card"],
            border_width=1,
            border_color=COLORS["border"],
        )
        defaults.update(kwargs)
        return ctk.CTkFrame(parent, **defaults)

    def make_section_label(self, parent, text: str) -> ctk.CTkLabel:
        return ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont("Segoe UI Semibold", 13),
            text_color=COLORS["text_primary"],
        )

    def make_label(self, parent, text: str, secondary=False) -> ctk.CTkLabel:
        return ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLORS["text_secondary"] if secondary else COLORS["text_primary"],
        )

    def make_entry(self, parent, placeholder="", show=None, width=320) -> ctk.CTkEntry:
        kwargs = dict(
            placeholder_text=placeholder,
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_muted"],
            font=ctk.CTkFont("Segoe UI", 12),
            width=width,
            corner_radius=6,
        )
        if show:
            kwargs["show"] = show
        return ctk.CTkEntry(parent, **kwargs)

    def make_button(self, parent, text, command, style="primary", width=120) -> ctk.CTkButton:
        styles = {
            "primary": dict(fg_color=COLORS["accent"], hover_color=COLORS["accent_dim"], text_color="#000000"),
            "secondary": dict(fg_color=COLORS["bg_input"], hover_color=COLORS["bg_hover"], text_color=COLORS["text_primary"], border_width=1, border_color=COLORS["border"]),
            "danger": dict(fg_color=COLORS["accent_red"], hover_color="#c0392b", text_color=COLORS["text_primary"]),
            "success": dict(fg_color=COLORS["accent_green"], hover_color="#2ea043", text_color="#000000"),
        }
        s = styles.get(style, styles["primary"])
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=ctk.CTkFont("Segoe UI Semibold", 12),
            corner_radius=8,
            width=width,
            height=36,
            **s,
        )

    def make_badge(self, parent, text: str, color: str) -> ctk.CTkLabel:
        return ctk.CTkLabel(
            parent,
            text=f" {text} ",
            font=ctk.CTkFont("Segoe UI Semibold", 10),
            text_color=color,
            fg_color=f"{color}22",
            corner_radius=4,
        )

    def show_status(self, label: ctk.CTkLabel, text: str, kind: str = "info"):
        color_map = {
            "info":    COLORS["text_secondary"],
            "success": COLORS["accent_green"],
            "error":   COLORS["accent_red"],
            "warning": COLORS["accent_yellow"],
        }
        label.configure(text=text, text_color=color_map.get(kind, COLORS["text_secondary"]))

    def on_show(self):
        """Called when this page is navigated to. Override to refresh data."""
        pass
