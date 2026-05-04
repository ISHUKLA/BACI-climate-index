# GitHub Publication Checklist

Before making the repository public:

1. Confirm that no private data, absolute local paths, or generated NetCDF files
   are committed.
2. Confirm that the data-source link in `docs/data_sources.md` is accessible to
   the intended audience.
3. Keep final notebooks under `notebooks/` for provenance, but use
   `src/baci_climate_index` as the reviewed implementation.
4. Run:

   ```bash
   python -m pip install -e ".[dev]"
   pytest
   ruff check .
   ```

5. Regenerate final outputs with:

   ```bash
   baci build-composite --config configs/default.yaml
   ```

6. Record the generated fingerprint from `outputs/BACI_fingerprint.json` in the
   release notes. Regenerate it whenever the methodology, weights, or input
   data change.

7. Add a license before publication if you want others to reuse the code.
8. Confirm that `CITATION.cff` renders correctly on GitHub.
9. Confirm that GitHub Actions passes on Python 3.10, 3.11, and 3.12.
10. Create a GitHub release from a version tag, then archive it with Zenodo.
