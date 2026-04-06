from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from src.styles import apply_plot_style

A4_PORTRAIT_SIZE_INCH = (8.27, 11.69)


def _contains_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def _format_range_text(start: pd.Timestamp, end: pd.Timestamp, is_cjk: bool) -> str:
    if is_cjk:
        return f"{start:%Y-%m} - {end:%Y-%m}"
    return f"{start:%b %Y} - {end:%b %Y}"


def _label_width_days(label: str, is_cjk: bool) -> float:
    # Rough width model for deciding left/right placement.
    unit = 11.0 if is_cjk else 7.5
    return max(55.0, len(label) * unit)


def _place_side_label(
    ax,
    text: str,
    y: float,
    bar_start: float,
    bar_end: float,
    x_min: float,
    x_max: float,
    en_font: str,
    zh_font: str,
) -> None:
    is_cjk = _contains_cjk(text)
    font_name = zh_font if is_cjk else en_font

    offset_days = 12.0
    estimated_width = _label_width_days(text, is_cjk)

    right_anchor = bar_end + offset_days
    right_fits = (right_anchor + estimated_width) <= x_max

    if right_fits:
        ax.text(
            right_anchor,
            y,
            text,
            va="center",
            ha="left",
            fontsize=10,
            fontweight="semibold",
            color="#111111",
            fontname=font_name,
            zorder=5,
            clip_on=False,
        )
    else:
        left_anchor = bar_start - offset_days
        ax.text(
            max(x_min + 1.0, left_anchor),
            y,
            text,
            va="center",
            ha="right",
            fontsize=10,
            fontweight="semibold",
            color="#111111",
            fontname=font_name,
            zorder=5,
            clip_on=False,
        )


def plot_gantt(
    data: pd.DataFrame,
    output_path: str,
    png_dpi: int = 600,
    row_height: float = 0.44,
) -> Path:
    """Draw an A4 portrait Gantt chart close to the reference slide style."""
    style_cfg = apply_plot_style()

    rows = len(data)
    fig = plt.figure(figsize=A4_PORTRAIT_SIZE_INCH)

    # Compact vertical block, wide usable horizontal area.
    ax = fig.add_axes([0.06, 0.40, 0.90, 0.31])

    y_step = 0.66
    y_positions = [(rows - 1 - i) * y_step for i in range(rows)]

    all_starts = mdates.date2num(data["Start"])
    all_ends = mdates.date2num(data["End"])
    x_min = all_starts.min() - 20
    x_max = all_ends.max() + 20
    ax.set_xlim(x_min, x_max)

    en_font = style_cfg["english_font"]
    zh_font = style_cfg["chinese_font"]

    for row_idx, (_, row) in enumerate(data.iterrows()):
        y = y_positions[row_idx]
        task_name = str(row["Task"])
        is_cjk_task = _contains_cjk(task_name)

        start_num = mdates.date2num(row["Start"])
        end_num = mdates.date2num(row["End"])

        if row["Type"] == "Task":
            duration = max(0.8, end_num - start_num)
            bar_end = start_num + duration

            ax.broken_barh(
                [(start_num, duration)],
                (y - row_height / 2, row_height),
                facecolors=style_cfg["task_color"],
                edgecolors=style_cfg["axes_facecolor"],
                linewidth=1.0,
                zorder=3,
            )

            # Date range inside bar.
            range_text = _format_range_text(row["Start"], row["End"], is_cjk_task)
            ax.text(
                start_num + duration / 2,
                y,
                range_text,
                va="center",
                ha="center",
                fontsize=10,
                fontweight="bold",
                color="#EAFBFF",
                fontname=(zh_font if is_cjk_task else en_font),
                zorder=4,
                clip_on=True,
            )

            # Task label near bar side (left or right based on available space).
            _place_side_label(
                ax=ax,
                text=task_name,
                y=y,
                bar_start=start_num,
                bar_end=bar_end,
                x_min=x_min,
                x_max=x_max,
                en_font=en_font,
                zh_font=zh_font,
            )

        else:
            ax.scatter(
                start_num,
                y,
                marker="D",
                s=52,
                color=style_cfg["milestone_color"],
                edgecolors=style_cfg["axes_facecolor"],
                linewidth=0.8,
                zorder=4,
            )

            _place_side_label(
                ax=ax,
                text=task_name,
                y=y,
                bar_start=start_num,
                bar_end=start_num,
                x_min=x_min,
                x_max=x_max,
                en_font=en_font,
                zh_font=zh_font,
            )

    ax.set_yticks([])

    top_y = y_positions[0] if y_positions else 0
    ax.set_ylim(-0.35, top_y + 1.02)

    # Year band at top.
    band_bottom = top_y + 0.60
    band_top = top_y + 0.96
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
                linewidth=0.9,
                zorder=3,
            )

        ax.text(
            (visible_start + visible_end) / 2,
            (band_bottom + band_top) / 2,
            str(year),
            va="center",
            ha="center",
            fontsize=10.5,
            fontweight="bold",
            color="#FFFFFF",
            fontname=en_font,
            zorder=4,
            clip_on=False,
        )

    ax.set_xlabel("")
    ax.set_xticks([])

    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs = {"dpi": png_dpi} if output.suffix.lower() == ".png" else {}

    fig.savefig(output, **save_kwargs)
    plt.close(fig)
    return output
