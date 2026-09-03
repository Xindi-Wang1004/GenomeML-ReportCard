"""Adapter: tabular train/test or split-column tables → canonical folds."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def adapt_tabular_membership(
    table_path: str | Path,
    id_col: str,
    split_col: str,
    *,
    train_values: tuple[str, ...] = ("train", "training"),
    test_values: tuple[str, ...] = ("test", "testing", "holdout"),
) -> dict[str, Any]:
    df = pd.read_csv(table_path, sep=None, engine="python")
    if id_col not in df.columns or split_col not in df.columns:
        raise KeyError(f"Need columns {id_col!r} and {split_col!r}; got {list(df.columns)}")
    train_ids = df.loc[df[split_col].astype(str).str.lower().isin(train_values), id_col].astype(str)
    test_ids = df.loc[df[split_col].astype(str).str.lower().isin(test_values), id_col].astype(str)
    folds = {"train": sorted(set(train_ids)), "test": sorted(set(test_ids))}
    return {
        "adapter": "tabular_membership",
        "n_train": len(folds["train"]),
        "n_test": len(folds["test"]),
        "id_overlap": len(set(folds["train"]) & set(folds["test"])),
        "folds": folds,
    }


def write_canonical(out_dir: str | Path, payload: dict[str, Any]) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "canonical_folds.json"
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path
