"""Plotting helpers for BACI outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from baci_climate_index.composite import decadal_means


def save_decadal_bar_chart(series: pd.Series, output_path: str | Path) -> Path:
    """Save a decadal BACI mean bar chart."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    means = decadal_means(series)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    means.plot(kind="bar", ax=ax, legend=False)
    ax.set_title("BACI - Decadal Mean")
    ax.set_xlabel("Decade")
    ax.set_ylabel("BACI")
    ax.axhline(0.0, color="black", linestyle="--", linewidth=0.8)
    fig.tight_layout()
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return output
