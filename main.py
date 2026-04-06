from __future__ import annotations

from pathlib import Path

import click

from src.parser import load_timeline_data
from src.plotter import plot_gantt

SUPPORTED_OUTPUT_FORMATS = ("pdf", "png", "svg")


def resolve_output_path(output_path: str, output_format: str) -> Path:
    path = Path(output_path)
    fmt = output_format.lower().strip()

    if path.suffix:
        suffix = path.suffix.lower().lstrip(".")
        if suffix not in SUPPORTED_OUTPUT_FORMATS:
            raise click.ClickException(
                f"Unsupported output suffix '{path.suffix}'. Use: .pdf, .png, .svg"
            )
        if suffix != fmt:
            raise click.ClickException(
                f"Output suffix '{path.suffix}' conflicts with --format {fmt}."
            )
        return path

    return path.with_suffix(f".{fmt}")


@click.command()
@click.option(
    "--input",
    "input_path",
    default="data_template.md",
    show_default=True,
    help="Input file path (.csv or .md).",
)
@click.option(
    "--output",
    "output_path",
    default="output/academic_gantt",
    show_default=True,
    help="Output path with or without extension.",
)
@click.option(
    "--format",
    "output_format",
    default="pdf",
    show_default=True,
    type=click.Choice(SUPPORTED_OUTPUT_FORMATS, case_sensitive=False),
    help="Output format when --output has no extension.",
)
def cli(input_path: str, output_path: str, output_format: str) -> None:
    """Generate an A4 portrait Gantt chart from CSV/Markdown data."""
    dataset = load_timeline_data(input_path)
    final_output_path = resolve_output_path(output_path, output_format)
    output_file = plot_gantt(data=dataset, output_path=str(final_output_path))

    click.echo(f"Chart generated: {output_file.resolve()}")
    click.echo(f"Rows parsed: {len(dataset)}")


if __name__ == "__main__":
    cli()
