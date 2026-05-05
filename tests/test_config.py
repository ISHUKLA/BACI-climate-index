from __future__ import annotations

from baci_climate_index.config import parse_config


def _raw_config(weights: dict[str, float] | None = None) -> dict[str, object]:
    return {
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
        "weights": weights or {},
        "options": {},
    }


def test_parse_config_resolves_relative_paths(tmp_path) -> None:
    config = parse_config(_raw_config({"sealevel_fs": 0.2}), base_dir=tmp_path)

    assert config.paths.components_dir == tmp_path / "data" / "composites"
    assert config.paths.output_dir == tmp_path / "outputs"


def test_parse_config_reads_sealevel_fs(tmp_path) -> None:
    config = parse_config(_raw_config({"sealevel_fs": 0.2}), base_dir=tmp_path)

    assert config.fs == 0.2


def test_parse_config_defaults_fs_to_public_value(tmp_path) -> None:
    config = parse_config(_raw_config(), base_dir=tmp_path)

    assert config.fs == 0.024
