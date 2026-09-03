"""Assertion provenance helpers for GenomeML Report Card."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

CLAIM_SOURCES = frozenset(
    {
        "author_declared",
        "upstream_release",
        "curator_mapped",
        "user_supplied",
        "remediation_only",
        "not_available",
    }
)
MEMBERSHIP_SOURCES = CLAIM_SOURCES | frozenset({"direct_release", "deterministic_generator"})
CURATION_STATUSES = frozenset(
    {"source_preserving", "adapter_only", "remediation_only", "user_supplied"}
)

ALLOWED = {
    "claim": CLAIM_SOURCES,
    "deployment_block": CLAIM_SOURCES,
    "unit_to_block_mapping": CLAIM_SOURCES,
    "split_membership": MEMBERSHIP_SOURCES,
    "curation_status": CURATION_STATUSES,
}


def validate_assertion_provenance(obj: Mapping[str, Any] | None) -> dict[str, str]:
    """Validate and return a normalized assertion_provenance dict.

    Raises ValueError on unknown keys or illegal enum values.
    Empty / None input returns {}.
    """
    if not obj:
        return {}
    out: dict[str, str] = {}
    for key, value in obj.items():
        if key not in ALLOWED:
            raise ValueError(
                f"assertion_provenance unknown field {key!r}; "
                f"allowed: {sorted(ALLOWED)}"
            )
        val = str(value).strip()
        if val not in ALLOWED[key]:
            raise ValueError(
                f"assertion_provenance.{key}={val!r} not in {sorted(ALLOWED[key])}"
            )
        out[key] = val
    return out


def load_assertion_provenance(path: Path | None) -> dict[str, str]:
    """Load assertion_provenance from JSON or YAML path."""
    if path is None:
        return {}
    text = path.read_text()
    data: Any
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise SystemExit("PyYAML required to load --assertion-provenance YAML") from exc
        raw = yaml.safe_load(text)
    else:
        import json

        raw = json.loads(text)
    if isinstance(raw, dict) and "assertion_provenance" in raw:
        raw = raw["assertion_provenance"]
    if not isinstance(raw, dict):
        raise ValueError("assertion_provenance file must contain an object")
    return validate_assertion_provenance(raw)
