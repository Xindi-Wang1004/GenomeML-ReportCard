# Publish this repository to GitHub

Local git is initialized on `main` (v0.1.3). Create the public remote once:

```bash
gh auth login
cd /Users/wangxindi/Desktop/sb/GenomeML-ReportCard
gh repo create Xindi-Wang1004/GenomeML-ReportCard --public --source=. --remote=origin --push
git tag -a v0.1.3 -m "genome-ml-reportcard 0.1.3"
git push origin v0.1.3
gh release create v0.1.3 --title "v0.1.3" --notes "Standalone GenomeML Report Card software repository."
```

Then refresh PyPI homepage URLs (already set in `pyproject.toml`) on the next `twine upload`.
