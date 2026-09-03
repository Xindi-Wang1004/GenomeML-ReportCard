#!/usr/bin/env python3
"""Generate toy manifests for CI: valid group-blocked split vs leaky split (contract fail)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TOY = HERE / "toy_data"
rng = np.random.default_rng(7)

n_groups, gpg, n_feat = 4, 5, 16
groups = np.repeat(np.arange(n_groups), gpg)
proto = rng.normal(size=(n_groups, n_feat))
X = np.vstack([proto[g] + 0.1 * rng.normal(size=n_feat) for g in groups])
y = groups.astype(float)

base = pd.DataFrame(
    {
        "sequence_id": [f"g{i}" for i in range(len(y))],
        "group": [f"sp{g}" for g in groups],
        "block": [f"blk{g}" for g in groups],
        "label": y,
    }
)

# Valid split: entire blocks in train OR test
valid = base.copy()
valid["split"] = np.where(valid["block"].isin(["blk0", "blk1"]), "train", "test")

# Leaky split: same block appears in train and test (should contract_status=fail)
leaky = base.copy()
leaky["split"] = np.where(leaky["sequence_id"].str.endswith(("0", "2", "4")), "train", "test")

TOY.mkdir(exist_ok=True)
base.to_csv(TOY / "manifest_with_block.tsv", sep="\t", index=False)
valid.to_csv(TOY / "manifest_valid_split.tsv", sep="\t", index=False)
leaky.to_csv(TOY / "manifest_leaky_split.tsv", sep="\t", index=False)
np.save(TOY / "X.npy", X)
print("wrote toy split manifests under", TOY)
