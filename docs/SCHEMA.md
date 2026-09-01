# GenomeML Report Card — report schema (v0.1.x)

## Required input columns (`SCHEMA_COLUMNS`)

| Field | Role |
|---|---|
| `sequence_id` (or accession alias) | Sequence / genome identifier |
| `label` | Target label |
| `group` (`--group` / `--label-unit`) | Label-assignment unit |

Optional: `block` (`--block` / `--deployment-block`; defaults to label unit), `split`, `taxonomy`, `fasta_path`.

## Validation behaviour

- **Hard failure:** missing required columns; unreadable table; mismatched feature matrix length.
- **Warning (emitted in JSON `probe.warnings`):** e.g. `ALL_SINGLETON_GROUPS`, `FEW_GROUPS` (n_blocks < 10).
- **Diagnostic flags (not hard failures):** high random-CV shared-block fraction; low within-block homogeneity; large `|Δ_B|` — these are reported for the user to interpret against the declared claim.

## Machine-readable output

JSON Schema: [`schemas/reportcard_report.schema.json`](schemas/reportcard_report.schema.json)

Validate a report (optional dependency `jsonschema`):

```bash
python -c "import json,jsonschema,pathlib; s=json.loads(pathlib.Path('schemas/reportcard_report.schema.json').read_text()); r=json.loads(pathlib.Path('tests/toy_data/report.json').read_text()); jsonschema.validate(r,s); print('OK')"
```

Toy valid report: `tests/toy_data/report.json`  
Invalid examples (for docs/CI): `tests/toy_data/invalid_missing_columns.json`
