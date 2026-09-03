# GenomeML Report Card

**Executable audit framework** for biological generalization claims in genome machine learning.

Existing tools answer *how to partition* (GroupKFold, CD-HIT, phylogenetic / temporal splits).  
GenomeML Report Card **records and audits mechanical consistency** with a user-declared holdout / deployment rule and emits a versioned, machine-readable evaluation contract. It does **not** choose the biologically correct deployment block.

| Package | `genome-ml-reportcard` |
|---------|------------------------|
| Install | `pip install genome-ml-reportcard` |
| License | MIT |
| Schema | [`schemas/reportcard_report.schema.json`](schemas/reportcard_report.schema.json) |

## Install

```bash
pip install genome-ml-reportcard
```

From this repository:

```bash
git clone https://github.com/Xindi-Wang1004/GenomeML-ReportCard.git
cd GenomeML-ReportCard
pip install -e ".[dev]"
pytest -q
```

## Quickstart

```bash
genome-ml-reportcard \
  --table manifest.tsv \
  --accession accession \
  --label-unit species \
  --deployment-block species \
  --label ogt_c \
  --features X_kmer4.npy \
  --out report/audit.json \
  --md-out report/audit.md
```

Aliases: `--group` ≡ `--label-unit`; `--block` ≡ `--deployment-block`.

### What the report checks

| Field | Meaning |
|-------|---------|
| `geometry.random_cv_shared_block_fraction` | Share of test rows whose block also appears in train under random CV |
| `geometry.within_block_homogeneity` | ICC (continuous) or majority purity (binary) within blocks |
| `probe.random` / `probe.blocked` | Locked-probe scores under random vs declared-block CV |
| `probe.delta` | Cohort-conditional contrast \(\Delta_B\) (not an external forecast) |
| `overlap` | Accession / block overlap when `--table-b` is provided |

Hard failures: missing required fields or feature/manifest length mismatch.  
Warnings: all-singleton groups, few blocks.

## Schema documentation

See [`docs/SCHEMA.md`](docs/SCHEMA.md). Validate reports against:

```text
schemas/reportcard_report.schema.json
```

## Interoperability

Report Card consumes **user-provided** fold / group columns. Typical upstream constructors:

- `sklearn.model_selection.GroupKFold` / `StratifiedGroupKFold`
- CD-HIT / MMseqs2 / Mash cluster IDs as `--deployment-block`
- phylogenetic clade or temporal batch columns
- any custom operational partition (site, country, collection year)

The tool audits consistency with the declaration; it does not replace those constructors.

## Examples and tutorials

- Toy valid / invalid reports: [`tests/toy_data/`](tests/toy_data/)
- Example contracts: [`examples/contracts/`](examples/contracts/)
- Tutorials: [`tutorials/`](tutorials/) (validate block-excluded split; detect recurrence; render report)

## Simulation

```bash
python simulate_label_geometry.py
```

Shows that \(\Delta_B\) depends on label geometry and can be near zero or **negative**.

## Citation

Wang et al., *GenomeML Report Card: an executable framework for auditing biological generalization claims in genome machine learning* (manuscript in preparation).

Software archive (concept DOI): [10.5281/zenodo.22275801](https://doi.org/10.5281/zenodo.22275801).  
Analysis companion (frozen tables / protocols): https://github.com/Xindi-Wang1004/GenomeML-ReportCard-companion

## License

MIT — see [`LICENSE`](LICENSE).
