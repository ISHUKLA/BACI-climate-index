"""Configuration loading for BACI workflows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class StudyConfig:
    """Calendar settings for the BACI study."""

    start_month: str
    end_month: str
    reference_start: str
    reference_end: str


@dataclass(frozen=True)
class PathConfig:
    """Input and output path settings."""

    components_dir: Path
    output_dir: Path


@dataclass(frozen=True)
class OptionsConfig:
    """Runtime switches for BACI construction."""

    make_decadal_png: bool = True
    require_no_missing: bool = True


@dataclass(frozen=True)
class BaciConfig:
    """Top-level BACI configuration."""

    study: StudyConfig
    paths: PathConfig
    components: dict[str, str]
    sealevel_weight: float
    options: OptionsConfig

    @property
    def component_paths(self) -> dict[str, Path]:
        """Return fully resolved component paths."""
        return {
            name: self.paths.components_dir / filename
            for name, filename in self.components.items()
        }


def load_config(path: str | Path) -> BaciConfig:
    """Load a YAML configuration file."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    return parse_config(raw, base_dir=config_path.parent)


def parse_config(raw: dict[str, Any], base_dir: Path | None = None) -> BaciConfig:
    """Parse a raw configuration dictionary."""
    base_dir = base_dir or Path.cwd()

    study_raw = raw["study"]
    paths_raw = raw["paths"]
    weights_raw = raw.get("weights", {})
    options_raw = raw.get("options", {})

    components_dir = _resolve_path(paths_raw["components_dir"], base_dir)
    output_dir = _resolve_path(paths_raw["output_dir"], base_dir)

    return BaciConfig(
        study=StudyConfig(
            start_month=study_raw["start_month"],
            end_month=study_raw["end_month"],
            reference_start=study_raw["reference_start"],
            reference_end=study_raw["reference_end"],
        ),
        paths=PathConfig(components_dir=components_dir, output_dir=output_dir),
        components=dict(raw["components"]),
        sealevel_weight=float(weights_raw.get("sealevel", 0.35)),
        options=OptionsConfig(
            make_decadal_png=bool(options_raw.get("make_decadal_png", True)),
            require_no_missing=bool(options_raw.get("require_no_missing", True)),
        ),
    )


def _resolve_path(value: str, base_dir: Path) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()
