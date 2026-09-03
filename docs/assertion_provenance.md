# Assertion provenance (contract field sources)

Mechanical conformance is assessed relative to the **recorded** evaluation contract.
`assertion_provenance` records **who declared** each contract field. It is not a
biological validation of the deployment block.

See also the paper analysis companion (`docs/assertion_provenance.md` and
`tables/Table_S_assertion_provenance.csv`).

## Allowed values

| Field | Allowed values |
|---|---|
| `claim` | `author_declared`, `upstream_release`, `curator_mapped`, `user_supplied`, `remediation_only`, `not_available` |
| `deployment_block` | same |
| `unit_to_block_mapping` | same |
| `split_membership` | same, plus `direct_release`, `deterministic_generator` |
| `curation_status` | `source_preserving`, `adapter_only`, `remediation_only`, `user_supplied` |

## Software interface

- JSON Schema: `schemas/reportcard_report.schema.json` → `assertion_provenance`
- CLI: `--assertion-provenance path/to/{json,yaml}`
- Module: `genome_ml_reportcard.assertion_provenance`
