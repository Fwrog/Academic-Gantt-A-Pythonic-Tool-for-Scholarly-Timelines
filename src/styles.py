from __future__ import annotations

import matplotlib as mpl

THEME = {
    "task_color": "#27B3BB",
    "milestone_color": "#1E4E82",
    "year_band_color": "#244F82",
    "year_divider_color": "#5F7FA7",
    "figure_facecolor": "#E7E7E7",
    "axes_facecolor": "#E7E7E7",
    "font_color": "#111111",
}


def apply_plot_style() -> dict:
    mpl.rcParams.update(
        {
            "font.size": 8,
            "axes.titlesize": 8,
            "axes.labelsize": 8,
            "axes.edgecolor": THEME["axes_facecolor"],
            "axes.linewidth": 0.8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans"],
            "text.color": THEME["font_color"],
            "axes.labelcolor": THEME["font_color"],
            "xtick.color": THEME["font_color"],
            "ytick.color": THEME["font_color"],
            "figure.facecolor": THEME["figure_facecolor"],
            "axes.facecolor": THEME["axes_facecolor"],
        }
    )
    return dict(THEME)
