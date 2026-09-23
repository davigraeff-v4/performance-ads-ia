#!/usr/bin/env python3
"""Busca seletiva na base local da Central de Ajuda do Google Ads.

Interface de linha de comando; o ranqueamento vive em `help_search.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from help_search import cli  # noqa: E402


if __name__ == "__main__":
    sys.exit(cli("google_ads", doc=__doc__))
