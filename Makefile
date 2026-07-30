.PHONY: validate test experiment-demo release-check clean-generated help

# Prefer local venv when present
PYTHON ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)
export PYTHONPATH := src:$(PYTHONPATH)

help:
	@echo "Targets: validate test experiment-demo release-check"

validate:
	$(PYTHON) -m school_security_audit.validate_metadata
	$(PYTHON) -m school_security_audit.validate_coding
	$(PYTHON) -m school_security_audit.validate_pilot_phase
	$(PYTHON) -m school_security_audit.validate_research_program
	$(PYTHON) -m school_security_audit.validate_todos
	$(PYTHON) -m school_security_audit.validate_phase_b
	$(PYTHON) -m school_security_audit.experiments

test:
	$(PYTHON) -m pytest -q

experiment-demo:
	$(PYTHON) -m school_security_audit.experiments

release-check: validate test
	@echo "Release-check OK (validators + tests + synthetic experiment demo)."

clean-generated:
	rm -rf experiments/_generated
