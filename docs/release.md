# Release and DOI Guide

Use this checklist when publishing a citable BACI Climate Index release.

## Before the release

1. Make sure the working tree is clean.
2. Run the local quality checks:

   ```bash
   python -m pip install -e ".[dev]"
   ruff check .
   pytest
   ```

3. Regenerate the BACI output from the documented configuration:

   ```bash
   baci build-composite --config configs/default.yaml
   ```

4. Compare the generated fingerprint with the reference values in
   `docs/github_checklist.md`.

## GitHub release

Create an annotated version tag and push it:

```bash
git tag -a v0.1.0 -m "BACI Climate Index v0.1.0"
git push origin v0.1.0
```

Then create a GitHub release from that tag. The release notes should mention:

- the BACI formula and reference period;
- the supported Python versions;
- where to obtain the source climate data;
- the fingerprint of the reproduced BACI series.

## Zenodo DOI

1. Enable the repository in the Zenodo GitHub integration.
2. Publish the GitHub release.
3. Wait for Zenodo to archive the release and mint a DOI.
4. Add the DOI to `README.md` and `CITATION.cff`.
5. Commit and release a patch version if the citation metadata changed after
   archiving.
