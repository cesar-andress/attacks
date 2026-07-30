"""Console entry points."""

from __future__ import annotations

from school_security_audit.validate_coding import main as validate_coding_main
from school_security_audit.validate_metadata import main as validate_metadata_main

__all__ = ["validate_coding_main", "validate_metadata_main"]
