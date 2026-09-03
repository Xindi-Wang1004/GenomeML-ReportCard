# GenomeML Report Card — release notes

## Summary

Executable evaluation-contract layer for genome / sequence ML: binds declared generalization claims to manifests, split artifacts, metrics, provenance, and standardized audit outcomes.

## Install

```bash
pip install genome-ml-reportcard
genome-ml-reportcard --help
```

## What's new

- Example contracts: Babayan (viral group / species), OGT species, Hu country, GenomicBenchmarks sequence holdout
- Tutorials: block-excluded split validation, declared-block recurrence detection, report rendering
- Expanded CI: schema validation, overlap, block recurrence, missing split artifact
- `assertion_provenance` schema field + CLI `--assertion-provenance`
- `environment.yml`, `CITATION.cff`, adapter stubs

## Schema / API

- Report JSON schema: `schemas/reportcard_report.schema.json` (includes `assertion_provenance`)
- CLI entry point: `genome-ml-reportcard`
- Python package: `genome_ml_reportcard`

## Known limitations

- Does not prescribe biologically correct blocks
- Does not infer fold membership when upstream releases omit it
- Large frozen C2 case registry and panel tables ship in the paper analysis companion repository, not in the PyPI wheel

## Reproduce minimal audit

```bash
git clone https://github.com/Xindi-Wang1004/GenomeML-ReportCard.git
cd GenomeML-ReportCard
pip install -e ".[dev]"
pytest -q
genome-ml-reportcard --help
```

## Archive

- GitHub: https://github.com/Xindi-Wang1004/GenomeML-ReportCard
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.22226465
- Paper analysis companion: https://github.com/Xindi-Wang1004/Spillover

## CI

GitHub Actions workflow runs on push/PR (see `.github/workflows/ci.yml`).
