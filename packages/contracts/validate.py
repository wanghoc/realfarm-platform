#!/usr/bin/env python3
"""Contract validation for packages/contracts.

Test skeleton for the shared JSON schemas (issue #8). Runs two checks:

1. meta-schema: every file in schemas/ is a valid JSON Schema against the
   meta-schema it declares in "$schema";
2. examples: every examples/<name>.valid.json validates against schemas/<name>.json,
   and every examples/<name>.invalid.json is rejected by it.

Usage (from anywhere):
    python packages/contracts/validate.py

Requires: jsonschema (see requirements.txt).
Exit code 0 on success, 1 on any failure — used by .github/workflows/ci-contracts.yml.
"""
from __future__ import annotations

import glob
import json
import os
import sys

from jsonschema import Draft202012Validator
from jsonschema.validators import validator_for

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(HERE, "schemas")
EXAMPLE_DIR = os.path.join(HERE, "examples")


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    failures = 0

    print("== meta-schema check ==")
    schemas: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(SCHEMA_DIR, "*.json"))):
        name = os.path.basename(path)[: -len(".json")]  # e.g. iot-measurement.v1
        schema = load(path)
        schemas[name] = schema
        cls = validator_for(schema)
        try:
            cls.check_schema(schema)
            print(f"  OK   {name} (meta: {cls.__name__})")
        except Exception as exc:  # noqa: BLE001 - report and continue
            failures += 1
            print(f"  FAIL {name}: {exc}")

    print("== example check ==")
    for path in sorted(glob.glob(os.path.join(EXAMPLE_DIR, "*.json"))):
        base = os.path.basename(path)
        key, kind, _ = base.rsplit(".", 2)  # iot-measurement.v1 . valid . json
        schema = schemas.get(key)
        if schema is None:
            failures += 1
            print(f"  FAIL {base}: no schema named '{key}'")
            continue
        errors = sorted(Draft202012Validator(schema).iter_errors(load(path)), key=str)
        if kind == "valid":
            if errors:
                failures += 1
                print(f"  FAIL {base}: expected valid, got: {errors[0].message}")
            else:
                print(f"  OK   {base} (valid)")
        elif kind == "invalid":
            if errors:
                print(f"  OK   {base} (rejected: {errors[0].message})")
            else:
                failures += 1
                print(f"  FAIL {base}: expected rejection, but it validated clean")
        else:
            failures += 1
            print(f"  FAIL {base}: name must end in .valid.json or .invalid.json")

    print()
    print("RESULT:", "PASS" if failures == 0 else f"FAIL ({failures})")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
