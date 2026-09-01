"""Contract status semantics for GenomeML Report Card audits."""
from __future__ import annotations

from typing import Any


# Status vocabulary used in JSON reports and manuscript Table 1b.
STATUS_FAIL = "fail"
STATUS_WARN = "warn"
STATUS_INFO = "info"
STATUS_PASS = "pass"


def evaluate_contract(
    *,
    geometry: dict[str, Any] | None = None,
    probe: dict[str, Any] | None = None,
    overlap: dict[str, Any] | None = None,
    user_split_block_recurrence: float | None = None,
) -> dict[str, Any]:
    """Return machine-readable contract_status + findings.

    Fail / warn / info rules (v0.1.2+):
    - fail: exact sequence ID overlap across compared partitions; user-provided
      blocked split with declared-block recurrence > 0
    - warn: ALL_SINGLETON_GROUPS / FEW_GROUPS; near-neighbor candidate overlap;
      severe block imbalance proxies already covered by FEW_GROUPS
    - info: high random-CV shared-block fraction; low within-block homogeneity;
      large |Δ_B| (interpretive, not invalidating)
    """
    findings: list[dict[str, str]] = []
    geometry = geometry or {}
    probe = probe or {}
    overlap = overlap or {}

    # --- Fail conditions ---
    exact = overlap.get("n_shared_accessions")
    if exact is None:
        exact = overlap.get("n_exact_id_overlap")
    if exact is not None and int(exact) > 0:
        findings.append(
            {
                "code": "EXACT_SEQUENCE_OVERLAP",
                "severity": STATUS_FAIL,
                "detail": f"exact_id_overlap={int(exact)}",
            }
        )

    if user_split_block_recurrence is not None and float(user_split_block_recurrence) > 0:
        findings.append(
            {
                "code": "DECLARED_BLOCK_RECURRENCE_IN_USER_SPLIT",
                "severity": STATUS_FAIL,
                "detail": (
                    "declared deployment block appears in both train and test "
                    f"(recurrence_fraction={float(user_split_block_recurrence):.4f})"
                ),
            }
        )

    # --- Warnings from probe ---
    for w in probe.get("warnings") or []:
        code = str(w).split(":", 1)[0].strip()
        findings.append({"code": code, "severity": STATUS_WARN, "detail": str(w)})

    nn = overlap.get("n_near_neighbor_candidate_pairs")
    if nn is None:
        nn = overlap.get("n_near_neighbor_hits")
    if nn is not None and int(nn) > 0:
        findings.append(
            {
                "code": "NEAR_NEIGHBOR_CANDIDATE_OVERLAP",
                "severity": STATUS_WARN,
                "detail": f"near_neighbor_candidate_pairs={int(nn)}",
            }
        )

    # --- Informational diagnostics ---
    shared = geometry.get("random_cv_shared_block_fraction")
    if shared is not None and float(shared) >= 0.5:
        findings.append(
            {
                "code": "HIGH_RANDOM_CV_SHARED_BLOCK_FRACTION",
                "severity": STATUS_INFO,
                "detail": (
                    f"random_cv_shared_block_fraction={float(shared):.3f}; "
                    "random estimand likely differs from block-held-out estimand"
                ),
            }
        )

    homog = geometry.get("within_block_homogeneity")
    if homog is not None and float(homog) < 0.5:
        findings.append(
            {
                "code": "LOW_WITHIN_BLOCK_HOMOGENEITY",
                "severity": STATUS_INFO,
                "detail": (
                    f"within_block_homogeneity={float(homog):.3f}; "
                    "Δ_B may be weak or non-monotone"
                ),
            }
        )

    delta = probe.get("delta")
    if delta is not None and abs(float(delta)) >= 0.2:
        findings.append(
            {
                "code": "LARGE_ABS_DELTA_B",
                "severity": STATUS_INFO,
                "detail": f"|Δ_B|={abs(float(delta)):.3f} under locked probe (cohort-conditional)",
            }
        )

    severities = {f["severity"] for f in findings}
    if STATUS_FAIL in severities:
        status = STATUS_FAIL
    elif STATUS_WARN in severities:
        status = STATUS_WARN
    elif findings:
        status = STATUS_PASS  # informational findings only → pass with notes
    else:
        status = STATUS_PASS

    return {
        "contract_status": status,
        "findings": findings,
        "n_fail": sum(1 for f in findings if f["severity"] == STATUS_FAIL),
        "n_warn": sum(1 for f in findings if f["severity"] == STATUS_WARN),
        "n_info": sum(1 for f in findings if f["severity"] == STATUS_INFO),
    }


def user_split_block_recurrence(df, split_col: str, block_col: str) -> float | None:
    """Fraction of test rows whose block also appears in train (mean over unique split labels).

    Expects binary-ish split labels containing 'train'/'test' (case-insensitive), or
    fold ids where we treat each fold as test once (GroupKFold-style columns named fold).
    """
    import numpy as np
    import pandas as pd

    if split_col not in df.columns or block_col not in df.columns:
        return None
    s = df[split_col].astype(str)
    b = df[block_col].astype(str)
    low = s.str.lower()
    if low.isin(["train", "test"]).all() or set(low.unique()) <= {"train", "test", "val", "valid", "validation"}:
        tr = b[low.eq("train")]
        te = b[low.isin(["test", "val", "valid", "validation"])]
        if len(te) == 0 or len(tr) == 0:
            return None
        train_blocks = set(tr)
        return float(np.mean([1.0 if x in train_blocks else 0.0 for x in te]))

    # fold ids: each unique value is a held-out fold
    fracs = []
    for fold in s.unique():
        te = b[s == fold]
        tr = b[s != fold]
        if len(te) == 0 or len(tr) == 0:
            continue
        train_blocks = set(tr)
        fracs.append(float(np.mean([1.0 if x in train_blocks else 0.0 for x in te])))
    if not fracs:
        return None
    return float(np.mean(fracs))
