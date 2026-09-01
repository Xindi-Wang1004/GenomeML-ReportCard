# Published-panel audit vignette (Babayan et al. 2018)

This vignette shows how GenomeML Report Card audits a **public** genome-ML panel
when the scientifically motivated deployment block differs from a naïve genome-
level random split.

## Panel

- **Study:** Babayan et al., *Science* 2018 (viral reservoir / host prediction)
- **Labels:** binary mammal vs other reservoir (`reservoir_host`; Orphan excluded)
- **Label-assignment unit:** species (often singleton in this panel)
- **Declared deployment block:** `Viral group` (12 phylogenetic / taxonomic groups)

## Claim being audited

A random genome-level CV score does **not** by itself support performance under
**held-out viral group** structure. Report Card records that declaration and
compares random vs Viral-group-blocked evaluation under a locked probe.

## Typical result (repeated CV companion)

| Protocol | AUROC |
|----------|------:|
| Random genome CV | ≈ 0.77 |
| Viral-group-blocked CV | ≈ 0.53 |
| \(\Delta_B\) | ≈ 0.24 |

Geometry: random-CV shared-block fraction ≈ 1.0; within-block majority purity ≈ 0.75.

## Command (once panel TSV + features are local)

```bash
genome-ml-reportcard \
  --table T08_babayan_viral_group.tsv \
  --accession accession \
  --label-unit species \
  --deployment-block "Viral group" \
  --label reservoir_host \
  --features X_kmer4.npy \
  --out T08_babayan_reportcard.json
```

Full machine-readable report from the manuscript bundle:
`multi_task_audit/results/published_audits/T08_babayan_reportcard.json`.

## What this does *not* claim

- That Babayan’s original modelling pipeline is invalid
- That `Viral group` is the unique correct biological holdout
- That blocked CV calibrates absolute external performance
