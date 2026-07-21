"""Shared pytest setup for the backend test suite.

The edge services (``simulator``, ``gateway``) import their shared code as a
top-level ``common`` package and run with ``backend/services`` as the root —
see ``.github/workflows/ci-simulator.yml`` and the service Dockerfiles. Put
that root on ``sys.path`` so tests can import and exercise the real listener
code, not a re-implementation of it.
"""

import sys
from pathlib import Path

_SERVICES_ROOT = Path(__file__).resolve().parent.parent / "services"
if str(_SERVICES_ROOT) not in sys.path:
    sys.path.insert(0, str(_SERVICES_ROOT))
