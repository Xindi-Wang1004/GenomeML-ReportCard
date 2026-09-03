# PyPI release (`genome-ml-reportcard`)

## Local verify

```bash
cd paper analysis companion/audit_toolkit
pip install -e ".[dev]"
python tests/test_smoke.py
pip install build
python -m build
```

## Publish (maintainer)

Current version: **0.1.1** (wheel in `dist/` and `00_to_upload/release/`).

1. Confirm `[project].version` in `pyproject.toml` matches `__version__`.
2. Push GitHub tag `reportcard-v0.1.1` (already created locally in Spillover_public_git).
3. Upload with PyPI token:

```bash
pip install twine
python3 -m twine upload dist/genome_ml_reportcard-0.1.1*
# username = __token__
# password = pypi-<API token>
```

4. Users install with:

```bash
pip install genome-ml-reportcard
genome-ml-reportcard --help
```

Zenodo: archive the same tag (GitHub→Zenodo or upload `00_to_upload/release/genome-ml-reportcard-v0.1.1-source.tgz`). Keep checkpoint DOI `10.5281/zenodo.21809791` separate.
