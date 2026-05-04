from __future__ import annotations

from baci_climate_index.config import parse_config


def test_parse_config_resolves_relative_paths(tmp_path) -> None:
    config = parse_config(
        {
            "study": {
                "start_month": "1961-01",
                "end_month": "2024-12",
                "reference_start": "1961-01-31",
                "reference_end": "1990-12-31",
            },
            "paths": {
                "components_dir": "data/composites",
                "output_dir": "outputs",
            },
            "components": {"precipitation": "precipitation_index.nc"},
            "weights": {"sealevel": 0.35},
            "options": {},
        },
        base_dir=tmp_path,
    )

    assert config.paths.components_dir == tmp_path / "data" / "composites"
    assert config.paths.output_dir == tmp_path / "outputs"
    assert config.sealevel_weight == 0.35
