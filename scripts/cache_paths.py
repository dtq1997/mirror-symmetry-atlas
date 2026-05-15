"""Shared local cache paths for maintenance scripts.

Curated YAML under data/ is the repository truth. Regenerable API responses,
HTML snapshots, and arXiv source trees live under .cache by default so Next.js
does not scan them during static builds.
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE_ROOT = Path(os.environ.get("MSA_CACHE_DIR", ROOT / ".cache/msa/papers"))


def cache_dir(name: str) -> Path:
    path = CACHE_ROOT / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def cache_path(name: str) -> str:
    return str(cache_dir(name))
