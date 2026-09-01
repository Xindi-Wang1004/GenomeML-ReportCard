#!/usr/bin/env python3
"""Label-geometry simulation: when does random vs group-blocked gap appear?

Generates synthetic features/labels with controllable ICC, within-group
replication, and feature correlation, then measures Δρ under the same
Ridge OOF probe contract as the empirical report card.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "third_domain_ogt_large" / "lib"))
from probe_lib import SEED, oof_ridge_spearman  # noqa: E402


def _make_dataset(
    n_groups: int,
    genomes_per_group: int,
    icc: float,
    within_corr: float,
    effect_size: float,
    label_noise: float,
    n_features: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """icc=1 → group-constant labels; icc=0 → independent genome labels."""
    groups = np.repeat(np.arange(n_groups), genomes_per_group)
    n = len(groups)
    # Group prototypes + within-group noise → feature correlation structure
    proto = rng.normal(0, 1, size=(n_groups, n_features))
    X = np.zeros((n, n_features))
    for g in range(n_groups):
        idx = groups == g
        shared = proto[g]
        noise = rng.normal(0, 1, size=(idx.sum(), n_features))
        X[idx] = np.sqrt(within_corr) * shared + np.sqrt(max(1e-8, 1 - within_corr)) * noise
    # Labels: group mean signal + optional within-group variation
    group_signal = rng.normal(0, 1, size=n_groups)
    y_group = effect_size * group_signal[groups]
    if icc >= 0.999:
        y = y_group + rng.normal(0, label_noise, size=n) * 0.0  # exact constant within group
        # tiny jitter avoided: keep exact constant for ICC≈1
        y = y_group.copy()
    else:
        within = rng.normal(0, 1, size=n)
        # approximate: Var(group)/(Var(group)+Var(within)) ≈ icc
        # y = sqrt(icc)*group + sqrt(1-icc)*within, scaled by effect
        y = effect_size * (
            np.sqrt(max(icc, 0)) * group_signal[groups]
            + np.sqrt(max(1e-8, 1 - icc)) * within
        )
        y = y + rng.normal(0, label_noise, size=n)
    return X.astype(float), y.astype(float), groups


def run_one(**kwargs) -> dict:
    panel = kwargs.pop("panel", "main")
    seed = int(kwargs.pop("seed", SEED))
    rng = np.random.default_rng(seed)
    X, y, groups = _make_dataset(rng=rng, **kwargs)
    rnd = oof_ridge_spearman(X, y, groups=None)
    blk = oof_ridge_spearman(X, y, groups=groups)
    rho_r = float(rnd["rho"]) if np.isfinite(rnd["rho"]) else float("nan")
    rho_b = float(blk["rho"]) if np.isfinite(blk["rho"]) else float("nan")
    return {
        "panel": panel,
        "seed": seed,
        **{k: kwargs[k] for k in kwargs},
        "n_genomes": int(len(y)),
        "random_rho": rho_r,
        "blocked_rho": rho_b,
        "delta_rho": rho_r - rho_b if np.isfinite(rho_r) and np.isfinite(rho_b) else float("nan"),
    }


def sweep(seed: int = SEED) -> pd.DataFrame:
    rows = []
    # Grid focused on ICC × replication (main GB claim); kept compact for CI
    for n_groups in (20,):
        for gpg in (1, 2, 5, 10):
            for icc in (0.0, 0.5, 1.0):
                for within_corr in (0.2, 0.8):
                    for effect_size in (1.5,):
                        rows.append(
                            run_one(
                                panel="main",
                                n_groups=n_groups,
                                genomes_per_group=gpg,
                                icc=icc,
                                within_corr=within_corr,
                                effect_size=effect_size,
                                label_noise=0.05,
                                n_features=32,
                                seed=seed,
                            )
                        )
    # Sign-reversal panel: low ICC + few groups → blocked CV high-variance;
    # Δ_B can be negative (blocked occasionally above random).
    for i, n_groups in enumerate((4, 6, 8)):
        for gpg in (5, 10):
            for icc in (0.0, 0.25):
                for within_corr in (0.2,):
                    rows.append(
                        run_one(
                            panel="sign_reversal",
                            n_groups=n_groups,
                            genomes_per_group=gpg,
                            icc=icc,
                            within_corr=within_corr,
                            effect_size=1.5,
                            label_noise=0.25,
                            n_features=32,
                            seed=seed + 1000 + i * 17 + gpg,
                        )
                    )
    # Multi-seed probe at one hostile geometry (few groups, ICC≈0)
    for s in range(seed, seed + 25):
        rows.append(
            run_one(
                panel="sign_reversal_multiseed",
                n_groups=6,
                genomes_per_group=5,
                icc=0.0,
                within_corr=0.2,
                effect_size=1.5,
                label_noise=0.25,
                n_features=32,
                seed=s,
            )
        )
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-csv", type=Path, default=ROOT / "tables" / "Table_simulation_label_geometry.csv")
    ap.add_argument("--out-json", type=Path, default=ROOT / "tables" / "Table_simulation_label_geometry_summary.json")
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()
    df = sweep(seed=args.seed)
    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out_csv, index=False)
    # Summary slices for manuscript
    main = df[df["panel"] == "main"]
    focus = main[(main["n_groups"] == 20) & (main["effect_size"] == 1.5) & (main["within_corr"] == 0.8)]
    rev = df[df["panel"] == "sign_reversal"]
    multi = df[df["panel"] == "sign_reversal_multiseed"]
    summary = {
        "seed": args.seed,
        "n_rows": len(df),
        "n_rows_main": int(len(main)),
        "singleton_mean_delta": float(main.loc[main["genomes_per_group"] == 1, "delta_rho"].mean()),
        "group_constant_icc1_gpg5_mean_delta": float(
            focus.loc[(focus["icc"] == 1.0) & (focus["genomes_per_group"] == 5), "delta_rho"].mean()
        ),
        "icc0_gpg5_mean_delta": float(
            focus.loc[(focus["icc"] == 0.0) & (focus["genomes_per_group"] == 5), "delta_rho"].mean()
        ),
        "main_n_negative_delta": int((main["delta_rho"] < 0).sum()),
        "main_min_delta": float(main["delta_rho"].min()),
        "sign_reversal_n_rows": int(len(rev)),
        "sign_reversal_n_negative": int((rev["delta_rho"] < 0).sum()),
        "sign_reversal_min_delta": float(rev["delta_rho"].min()) if len(rev) else None,
        "sign_reversal_example": (
            rev.loc[rev["delta_rho"].idxmin(), ["n_groups", "genomes_per_group", "icc", "random_rho", "blocked_rho", "delta_rho"]]
            .astype(float)
            .to_dict()
            if len(rev)
            else None
        ),
        "multiseed_n": int(len(multi)),
        "multiseed_frac_negative_delta": float((multi["delta_rho"] < 0).mean()) if len(multi) else None,
        "multiseed_mean_delta": float(multi["delta_rho"].mean()) if len(multi) else None,
        "out_csv": str(args.out_csv),
    }
    args.out_json.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print("wrote", args.out_csv)


if __name__ == "__main__":
    main()
