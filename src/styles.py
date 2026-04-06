from __future__ import annotations

import matplotlib as mpl
from matplotlib import font_manager

# Palette extracted from reference slides:
# background gray + navy year band + cyan task bars.
THEME = {
    "task_color": "#19B7BE",
    "milestone_color": "#1F4F84",
    "year_band_color": "#244F82",
    "year_divider_color": "#5C7CA3",
    "figure_facecolor": "#E6E6E6",
    "axes_facecolor": "#E6E6E6",
    "font_color": "#111111",
}

ENGLISH_FONT_CANDIDATES = ["Arial", "Liberation Sans", "DejaVu Sans"]
CHINESE_FONT_CANDIDATES = [
    "SimSun",
    "NSimSun",
    "Songti SC",
    "STSong",
    "Microsoft YaHei",
    "SimHei",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "PingFang SC",
    "WenQuanYi Zen Hei",
]


def _first_available(candidates: list[str], installed: set[str], fallback: str) -> str:
    for font_name in candidates:
        if font_name in installed:
            return font_name
    return fallback


def resolve_language_fonts() -> tuple[str, str]:
    installed = {font.name for font in font_manager.fontManager.ttflist}
    english_font = _first_available(ENGLISH_FONT_CANDIDATES, installed, "DejaVu Sans")
    chinese_font = _first_available(CHINESE_FONT_CANDIDATES, installed, english_font)
    return english_font, chinese_font


def apply_plot_style() -> dict:
    en_font, zh_font = resolve_language_fonts()
    mpl.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 10,
            "axes.labelsize": 10,
            "axes.edgecolor": THEME["axes_facecolor"],
            "axes.linewidth": 0.8,
            "xtick.labelsize": 9,
            "ytick.labelsize": 10,
            "font.family": "sans-serif",
            "font.sans-serif": [en_font, zh_font, "DejaVu Sans"],
            "axes.unicode_minus": False,
            "text.color": THEME["font_color"],
            "axes.labelcolor": THEME["font_color"],
            "xtick.color": THEME["font_color"],
            "ytick.color": THEME["font_color"],
            "figure.facecolor": THEME["figure_facecolor"],
            "axes.facecolor": THEME["axes_facecolor"],
        }
    )
    return {**THEME, "english_font": en_font, "chinese_font": zh_font}
