#!/usr/bin/env python3
"""CLI wrapper: validate coding templates / records."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from school_security_audit.validate_coding import main

if __name__ == "__main__":
    raise SystemExit(main())
