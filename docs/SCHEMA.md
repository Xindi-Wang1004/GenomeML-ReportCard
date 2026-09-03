# GenomeML Report Card — report schema

## Required input columns (`SCHEMA_COLUMNS`)

| Field | Role |
|---|---|
| `sequence_id` (or accession alias) | Sequence / genome identifier |
| `label` | Target label |
| `group` (`--group` / `--label-unit`) | Label-assignment unit |

Optional: `block` (`--block` / `--deployment-block`; defaults to label unit), `--split` (user folds), `--deployment-claim`, `assertion_provenance`, `taxonomy`, `fasta_path`.

## Assertion provenance (`assertion_provenance`)

Optional object recording **who declared** each contract field. Mechanical conformance is assessed relative to the recorded contract; this object separates author-declared fields from curator-mapped, user-supplied, or remediation-only fields.

| Field | Allowed values |
|---|---|
| `claim` | `author_declared` / `upstream_release` / `curator_mapped` / `user_supplied` / `remediation_only` / `not_available` |
| `deployment_block` | same |
| `unit_to_block_mapping` | same |
| `split_membership` | same, plus `direct_release` / `deterministic_generator` when recording membership provenance |
| `curation_status` | `source_preserving` / `adapter_only` / `remediation_only` / `user_supplied` |

## Contract status (`contract_status`)

Overall status plus `contract.findings[]` with severity `fail` | `warn` | `info`.

| Audit condition | Status | Interpretation |
|---|---|---|
| Required fields absent / feature–table mismatch | **Fail** (hard exit) | Contract cannot be evaluated |
| Exact sequence-ID overlap (`--table-b`) | **Fail** | Partition contamination risk |
| User `--split` with declared-block recurrence > 0 | **Fail** | Split contradicts declared holdout rule |
| Near-neighbor candidate overlap | **Warn** | Needs sequence-level review |
| All-singleton / few blocks (`n_blocks<10`) | **Warn** | Unstable or ≈ random by construction |
| High random-CV shared-block fraction (≥0.5) | **Info** | Random estimand ≠ block-held-out |
| Low within-block homogeneity (<0.5) | **Info** | \(\Delta_B\) may be weak/non-monotone |
| Large \(\|\Delta_B\|\) (≥0.2) | **Info** | Cohort-conditional; not external forecast |

See also `tables/Table_contract_status_rules.md` in the paper companion.

## Machine-readable output

JSON Schema: [`schemas/reportcard_report.schema.json`](../schemas/reportcard_report.schema.json)

Toy valid report: `tests/toy_data/report.json`
