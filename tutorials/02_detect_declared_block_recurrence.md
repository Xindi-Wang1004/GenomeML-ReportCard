# Tutorial 2: Detect deliberate declared-block recurrence (~5 min)

```bash
# Toy leaky split fixture:
ls tests/toy_data/manifest_leaky_split.tsv
python -m pytest tests/test_adoption_demo.py -q
```

Expect: recurrence > 0 under a strict contract → nonconformant / fail relative to the declared contract (not a claim that the study is scientifically invalid).
