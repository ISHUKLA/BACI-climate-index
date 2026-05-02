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

6. Compare the generated fingerprint with the final reference:

   ```text
   mean: 0.27409226621375793
   std:  0.5843940951495518
   head: [-0.036153, 0.834808, 0.339282]
   tail: [0.582361, 0.6512, 0.54511]
   ```

7. Add a license before publication if you want others to reuse the code.
