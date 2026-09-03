#!/usr/bin/env python3
"""End-to-end adoption demo: pass audit vs split-fail contract."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOY = HERE / "toy_data"
PKG = HERE.parent


def _run(args: list[str]) -> dict:
    cmd = [sys.executable, "-m", "genome_ml_reportcard.cli", *args]
    subprocess.run(cmd, cwd=str(PKG), check=True)
    out = Path(args[args.index("--out") + 1])
    return json.loads(out.read_text())


def main() -> None:
    # baseline pass (group-constant labels, large Δ_B)
    rep_pass = _run(
        [
            "--table",
            str(TOY / "manifest.tsv"),
            "--features",
            str(TOY / "X.npy"),
            "--out",
            str(TOY / "report_pass.json"),
        ]
    )
    assert rep_pass["contract_status"] in {"pass", "warn"}, rep_pass["contract_status"]
    assert rep_pass["probe"]["delta"] > 0.3

    # valid user split → pass (no block recurrence)
    rep_valid = _run(
        [
            "--table",
            str(TOY / "manifest_valid_split.tsv"),
            "--features",
            str(TOY / "X.npy"),
            "--group",
            "group",
            "--block",
            "block",
            "--split",
            "split",
            "--deployment-claim",
            "held-out composition block",
            "--out",
            str(TOY / "report_valid_split.json"),
        ]
    )
    assert rep_valid["contract_status"] != "fail", rep_valid

    # leaky user split → fail
    rep_fail = _run(
        [
            "--table",
            str(TOY / "manifest_leaky_split.tsv"),
            "--features",
            str(TOY / "X.npy"),
            "--group",
            "group",
            "--block",
            "block",
            "--split",
            "split",
            "--deployment-claim",
            "held-out composition block (INVALID: block leaks)",
            "--out",
            str(TOY / "report_fail_split.json"),
        ]
    )
    assert rep_fail["contract_status"] == "fail", rep_fail["contract_status"]
    rec = rep_fail["user_split_audit"]["declared_block_recurrence_fraction"]
    assert rec > 0, rec

    print("ADOPTION_DEMO_OK", rep_pass["contract_status"], rep_valid["contract_status"], rep_fail["contract_status"])


if __name__ == "__main__":
    main()
