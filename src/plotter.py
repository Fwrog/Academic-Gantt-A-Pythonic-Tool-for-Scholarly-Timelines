from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from src.styles import apply_plot_style

A4_PORTRAIT_SIZE_INCH = (8.27, 11.69)


def plot_gantt(data: pd.DataFrame, output_path: str, row_height: float = 0.34) -> Path:
    """Draw an A4-portrait Gantt chart with compact spacing."""
    style_cfg = apply_plot_style()

    rows = len(data)
    fig = plt.figure(figsize=A4_PORTRAIT_SIZE_INCH)
    ax = fig.add_axes([0.24, 0.33, 0.70, 0.43])

    y_step = 0.72
    y_positions = [(rows - 1 - i) * y_step for i in range(rows)]

    for row_idx, (_, row) in enumerate(data.iterrows()):
        y = y_positions[row_idx]
        start_num = mdates.date2num(row["Start"])

        if row["Type"] == "Task":
            end_num = mdates.date2num(row["End"])
            duration = max(0.7, end_num - start_num)
            ax.broken_barh(
                [(start_num, duration)],
                (y - row_height / 2, row_height),
                facecolors=style_cfg["task_color"],
                edgecolors=style_cfg["axes_facecolor"],
                linewidth=1.0,
                zorder=3,
            )
        else:
            ax.scatter(
                start_num,
                y,
                marker="D",
                s=32,
                color=style_cfg["milestone_color"],
                edgecolors=style_cfg["axes_facecolor"],
                linewidth=0.7,
                zorder=4,
            )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(data["Task"].tolist(), fontweight="semibold")

    all_starts = mdates.date2num(data["Start"])
    all_ends = mdates.date2num(data["End"])
    margin_days = 35
    x_min = all_starts.min() - margin_days
    x_max = all_ends.max() + margin_days
    ax.set_xlim(x_min, x_max)

    top_y = y_positions[0] if y_positions else 0
    ax.set_ylim(-0.35, top_y + 0.95)

    band_bottom = top_y + 0.53
    band_top = top_y + 0.83
    ax.axhspan(band_bottom, band_top, color=style_cfg["year_band_color"], zorder=2)

    first_year = int(data["Start"].min().year)
    last_year = int(data["End"].max().year)
    for year in range(first_year, last_year + 1):
        year_start = mdates.date2num(pd.Timestamp(year=year, month=1, day=1))
        year_end = mdates.date2num(pd.Timestamp(year=year + 1, month=1, day=1))

        visible_start = max(year_start, x_min)
        visible_end = min(year_end, x_max)
        if visible_end <= visible_start:
            continue

        if year > first_year and year_start <= x_max:
            ax.plot(
                [year_start, year_start],
                [band_bottom, band_top],
                color=style_cfg["year_divider_color"],
                linewidth=0.8,
                zorder=3,
            )

        ax.text(
            (visible_start + visible_end) / 2,
            (band_bottom + band_top) / 2,
            str(year),
            va="center",
            ha="center",
            fontsize=8,
            fontweight="bold",
            color="#FFFFFF",
            zorder=4,
            clip_on=False,
        )

    ax.set_xlabel("")
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0, pad=4)

    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs = {"dpi": 320} if output.suffix.lower() == ".png" else {}

    fig.savefig(output, **save_kwargs)
    plt.close(fig)
    return output
