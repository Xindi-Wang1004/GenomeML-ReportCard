#!/usr/bin/env bash
# Prepare local GenomeML-ReportCard v0.2.0 artifacts (does NOT push / upload).
# Run from GenomeML-ReportCard root after review.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== version pins =="
python3 - <<'PY'
from pathlib import Path
import re
init = Path("genome_ml_reportcard/__init__.py").read_text()
py = Path("pyproject.toml").read_text()
cff = Path("CITATION.cff").read_text() if Path("CITATION.cff").exists() else ""
v_init = re.search(r'__version__\s*=\s*"([^"]+)"', init).group(1)
v_py = re.search(r'^version\s*=\s*"([^"]+)"', py, re.M).group(1)
assert v_init == v_py == "0.2.0", (v_init, v_py)
print("OK local version", v_init)
if cff:
    assert "version: 0.2.0" in cff
    print("OK CITATION.cff")
PY

echo "== tests =="
python3 -m pytest -q tests/test_assertion_provenance.py tests/test_adoption_demo.py 2>/dev/null || python3 -m pytest -q tests/test_assertion_provenance.py

echo "== build sdist/wheel =="
python3 -m build 2>/dev/null || pip install -q build && python3 -m build

echo "== next human steps (requires auth) =="
cat <<'EOF'
1. Commit remaining GenomeML-ReportCard changes (assertion_provenance, schema, docs).
2. git tag -a v0.2.0 -m "GenomeML Report Card v0.2.0"
3. git push origin main && git push origin v0.2.0
4. gh release create v0.2.0 --title "v0.2.0" --notes-file RELEASE_v0.2.0.md
5. twine upload dist/genome_ml_reportcard-0.2.0*
6. Confirm Zenodo deposits a version DOI from the GitHub release; update MS if needed.
7. Include Hu frozen package from Spillover paper analysis companion/.../C2-HU-MSMA-LOSO-OUTER in Zenodo archive notes.
EOF
