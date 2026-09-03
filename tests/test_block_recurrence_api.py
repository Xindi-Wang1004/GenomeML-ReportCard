from __future__ import annotations

import pandas as pd
import pytest

from genome_ml_reportcard.contract import evaluate_contract, user_split_block_recurrence


def test_zero_recurrence_conformant():
    df = pd.DataFrame(
        {
            "split": ["train", "train", "test", "test"],
            "block": ["A", "A", "B", "B"],
        }
    )
    rec = user_split_block_recurrence(df, "split", "block")
    assert rec == 0.0
    out = evaluate_contract(user_split_block_recurrence=rec)
    assert out["contract_status"] == "pass"


def test_positive_recurrence_nonconformant():
    df = pd.DataFrame(
        {
            "split": ["train", "train", "test", "test"],
            "block": ["A", "B", "A", "C"],
        }
    )
    rec = user_split_block_recurrence(df, "split", "block")
    assert rec > 0.0
    out = evaluate_contract(user_split_block_recurrence=rec)
    assert out["contract_status"] == "fail"
