"""Adapter: integer index arrays / dict of indices → canonical membership via ID list."""
from __future__ import annotations

from typing import Any, Sequence


def adapt_indexed_split(
    ids: Sequence[str],
    train_idx: Sequence[int],
    test_idx: Sequence[int],
) -> dict[str, Any]:
    ids = [str(x) for x in ids]
    train = [ids[i] for i in train_idx]
    test = [ids[i] for i in test_idx]
    return {
        "adapter": "indexed_split",
        "n_train": len(train),
        "n_test": len(test),
        "id_overlap": len(set(train) & set(test)),
        "folds": {"train": train, "test": test},
    }
