"""Shared matplotlib style + footer helpers."""
from __future__ import annotations

import datetime as dt
import subprocess
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.linestyle": ":",
    "grid.alpha": 0.4,
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})


def git_short_sha(repo_root: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=4,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        pass
    return "no-git"


_REPO_ROOT = Path(r"C:\Users\Gebruiker\Documents\gevoelscore-app")
_RUN_STAMP = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
_GIT_SHA = git_short_sha(_REPO_ROOT)


def stamp_footer(fig, extra: str | None = None) -> None:
    parts = [f"stress_low_motion_viz", f"run {_RUN_STAMP}", f"sha {_GIT_SHA}"]
    if extra:
        parts.append(extra)
    fig.text(
        0.99, 0.01, "  ·  ".join(parts),
        ha="right", va="bottom", fontsize=7, color="#888",
    )


def savefig(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    print(f"  wrote {path.name}")
