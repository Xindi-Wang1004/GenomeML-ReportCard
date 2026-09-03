from pathlib import Path

import pytest

from genome_ml_reportcard.assertion_provenance import (
    load_assertion_provenance,
    validate_assertion_provenance,
)


def test_validate_ok():
    obj = validate_assertion_provenance(
        {
            "claim": "author_declared",
            "deployment_block": "upstream_release",
            "unit_to_block_mapping": "upstream_release",
            "split_membership": "direct_release",
            "curation_status": "source_preserving",
        }
    )
    assert obj["split_membership"] == "direct_release"


def test_validate_rejects_bad_enum():
    with pytest.raises(ValueError, match="deployment_block"):
        validate_assertion_provenance({"deployment_block": "invented"})


def test_load_nested_json(tmp_path: Path):
    p = tmp_path / "ap.json"
    p.write_text(
        '{"assertion_provenance": {"claim": "user_supplied", '
        '"curation_status": "user_supplied"}}'
    )
    assert load_assertion_provenance(p)["claim"] == "user_supplied"
