# GenomeML Report Card v0.1.3

- **contract_status:** `warn`
- rows: 20
- label-assignment groups: 4
- label unit column: `group`
- blocking unit column: `block`
- deployment claim (user-declared): held-out composition block

## Label geometry

- within-block homogeneity (ICC): 1.0
- within-label-unit homogeneity: 1.0
- n blocks: 4
- median block size: 5.0
- % singleton blocks: 0.0
- random-CV shared-block fraction: 1.0

## Contract findings

- **warn** `FEW_GROUPS`: FEW_GROUPS: n_blocks<10; interpret contrasts cautiously
- **info** `HIGH_RANDOM_CV_SHARED_BLOCK_FRACTION`: random_cv_shared_block_fraction=1.000; random estimand likely differs from block-held-out estimand
- **info** `LARGE_ABS_DELTA_B`: |Δ_B|=0.969 under locked probe (cohort-conditional)

## Split-design contrast

- primary metric: rho
- random: 0.9694584179118516
- blocked: 0.0
- Δ: 0.9694584179118516
- Δρ (always reported): 0.9694584179118516
- n_blocks: 4
- frac singleton blocks: 0.0

- **WARNING:** FEW_GROUPS: n_blocks<10; interpret contrasts cautiously
