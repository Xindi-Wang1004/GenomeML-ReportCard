"""Schema smoke + conceptual four-axis labels used by analysis companion."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_report_schema_loads():
    schema = json.loads((ROOT / "schemas/reportcard_report.schema.json").read_text())
    assert schema.get("type") == "object" or "$schema" in schema or "properties" in schema


def test_example_contracts_exist():
    d = ROOT / "examples/contracts"
    for name in [
        "babayan_viral_group.yaml",
        "babayan_species.yaml",
        "ogt_species.yaml",
        "hu_country.yaml",
        "genomicbenchmarks_sequence.yaml",
    ]:
        assert (d / name).is_file()


def test_toy_valid_and_leaky_manifests():
    assert (ROOT / "tests/toy_data/manifest_valid_split.tsv").is_file()
    assert (ROOT / "tests/toy_data/manifest_leaky_split.tsv").is_file()


def test_four_axis_vocabulary_documented():
    # Soft check: README or CHANGELOG mentions axes or v0.2.0
    text = (ROOT / "CHANGELOG.md").read_text()
    assert "0.2.0" in text
