# Tutorial 1: Validate a declared block-excluded split (~5 min)

```bash
pip install -e .
genome-ml-reportcard --help
# Using toy valid split:
python -m pytest tests/test_adoption_demo.py -q
```

Contract sketch: see `examples/contracts/babayan_viral_group.yaml`.
Expect: zero fold-local block recurrence under a strict exclusion contract → conformant / pass.
