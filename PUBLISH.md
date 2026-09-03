# Publish GenomeML Report Card v0.2.0

## 1. Pre-flight

```bash
cd GenomeML-ReportCard
python3 -c "import genome_ml_reportcard as g; print(g.__version__)"
grep '^version' pyproject.toml
pytest -q
python3 -m build
genome-ml-reportcard --help
```

Expected version: **0.2.0** everywhere.

## 2. GitHub release

```bash
git remote add origin https://github.com/Xindi-Wang1004/GenomeML-ReportCard.git  # if missing
git add -A
git commit -m "Release v0.2.0: contracts, tutorials, assertion provenance, expanded CI."
git tag -a v0.2.0 -m "GenomeML Report Card v0.2.0"
git push origin main
git push origin v0.2.0
gh release create v0.2.0 --title "v0.2.0" --notes-file RELEASE_v0.2.0.md
```

## 3. PyPI

```bash
pip install twine build
python3 -m build
python3 -m twine upload dist/genome_ml_reportcard-0.2.0*
```

## 4. Zenodo

1. Link this GitHub repo to Zenodo (or upload `dist/*.tar.gz`)
2. Mint a **version DOI** under concept DOI `10.5281/zenodo.22226465`
3. Record the version DOI + source SHA-256 in the paper analysis companion hash table

## 5. Manuscript update

After the version DOI exists, update Data availability with the version DOI + commit hash.
Do **not** put journal names or internal working-folder names in public README / release notes.
