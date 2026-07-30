"""Console entry points."""

from __future__ import annotations

from school_security_audit.validate_coding import main as validate_coding_main
from school_security_audit.validate_metadata import main as validate_metadata_main
from school_security_audit.validate_pilot_phase import main as validate_pilot_phase_main
from school_security_audit.validate_research_program import (
    main as validate_research_program_main,
)

__all__ = [
    "validate_coding_main",
    "validate_metadata_main",
    "validate_pilot_phase_main",
    "validate_research_program_main",
]
