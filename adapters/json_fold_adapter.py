"""Adapter: JSON list-of-folds (Hu-style) → canonical fold membership."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def adapt_json_folds(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text())
    if not isinstance(data, list):
        raise ValueError("Expected a JSON list of folds (each fold = list of IDs)")
    folds = {f"fold_{i:02d}": [str(x) for x in fold] for i, fold in enumerate(data)}
    all_ids = [g for f in folds.values() for g in f]
    multi = len(all_ids) - len(set(all_ids))
    return {
        "adapter": "json_fold",
        "n_folds": len(folds),
        "n_ids": len(set(all_ids)),
        "ids_in_multiple_test_folds": multi,
        "folds": folds,
    }
