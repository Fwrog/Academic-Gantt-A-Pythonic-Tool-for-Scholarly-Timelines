from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["Task", "Start", "End", "Type"]

COLUMN_ALIASES = {
    "Task": {"task", "任务", "任务名称", "项目", "阶段"},
    "Start": {"start", "开始", "开始日期"},
    "End": {"end", "结束", "结束日期"},
    "Type": {"type", "类型", "节点类型"},
    # Optional legacy column: keep compatibility if provided.
    "Resource": {"resource", "资源", "类别", "任务类别", "分组"},
}

TYPE_ALIASES = {
    "task": {"task", "任务", "工作", "阶段", "普通任务"},
    "milestone": {"milestone", "里程碑", "节点", "关键节点"},
}


def load_timeline_data(input_path: str) -> pd.DataFrame:
    """Load and validate timeline data from CSV or Markdown table."""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in {".md", ".markdown"}:
        df = _read_markdown_table(path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}. Use .csv, .md, or .markdown.")

    return _validate_dataframe(df)


def _read_markdown_table(path: Path) -> pd.DataFrame:
    """Convert a markdown table into a pandas DataFrame."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    table_lines = []
    for line in lines:
        normalized = line.lstrip("\ufeff").strip()
        if normalized.startswith("|"):
            table_lines.append(normalized)

    if len(table_lines) < 2:
        raise ValueError("No valid markdown table found. The file should contain a pipe table.")

    normalized_rows = []
    for idx, line in enumerate(table_lines):
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if idx == 1 and all(set(cell).issubset({"-", ":"}) for cell in cells):
            continue
        normalized_rows.append(",".join(cells))

    csv_like = "\n".join(normalized_rows)
    return pd.read_csv(StringIO(csv_like))


def _normalize_column_name(name: str) -> str:
    return str(name).replace("\ufeff", "").strip().lower()


def _canonicalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map: dict[str, str] = {}
    occupied_targets: set[str] = set()

    for col in df.columns:
        normalized_col = _normalize_column_name(col)
        target = None
        for canonical, aliases in COLUMN_ALIASES.items():
            if normalized_col in aliases:
                target = canonical
                break

        if target and target not in occupied_targets:
            rename_map[col] = target
            occupied_targets.add(target)
        else:
            rename_map[col] = str(col).replace("\ufeff", "").strip()

    return df.rename(columns=rename_map).copy()


def _normalize_type_value(raw_type: str) -> str:
    value = str(raw_type).strip().lower()
    for canonical, aliases in TYPE_ALIASES.items():
        if value in aliases:
            return canonical
    return value


def _validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = _canonicalize_columns(df)

    missing = [col for col in REQUIRED_COLUMNS if col not in clean_df.columns]
    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing)
            + ". Required/Supported headers: Task(任务), Start(开始), End(结束), Type(类型)."
        )

    clean_df["Task"] = clean_df["Task"].astype(str).str.strip()
    clean_df["Type"] = clean_df["Type"].astype(str).map(_normalize_type_value)

    clean_df["Start"] = pd.to_datetime(clean_df["Start"], format="%Y-%m-%d", errors="coerce")
    clean_df["End"] = pd.to_datetime(clean_df["End"], format="%Y-%m-%d", errors="coerce")

    if clean_df["Task"].eq("").any():
        raise ValueError("Column 'Task/任务' contains empty values.")
    if clean_df["Start"].isna().any():
        raise ValueError("Column 'Start/开始' contains invalid dates. Use YYYY-MM-DD.")
    if clean_df["End"].isna().any():
        raise ValueError("Column 'End/结束' contains invalid dates. Use YYYY-MM-DD.")

    invalid_types = sorted(set(clean_df["Type"]) - set(TYPE_ALIASES.keys()))
    if invalid_types:
        raise ValueError(
            "Column 'Type/类型' has invalid values: "
            + ", ".join(invalid_types)
            + ". Supported: Task/任务, Milestone/里程碑."
        )

    task_rows = clean_df["Type"] == "task"
    if (clean_df.loc[task_rows, "End"] < clean_df.loc[task_rows, "Start"]).any():
        raise ValueError("Task/任务 rows must satisfy End >= Start.")

    milestone_rows = clean_df["Type"] == "milestone"
    clean_df.loc[milestone_rows, "End"] = clean_df.loc[milestone_rows, "Start"]

    clean_df["Type"] = clean_df["Type"].str.title()
    clean_df = clean_df.sort_values(["Start", "Type", "Task"], kind="stable").reset_index(drop=True)
    return clean_df
