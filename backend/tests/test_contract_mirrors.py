"""Contract-mirror regression tests.

Several backend models declare they "mirror" a JSON Schema in
``packages/contracts/schemas`` (``PlayerActionRequestV1`` mirrors
``player-action-request.v1.json``; ``AutomationCommandV1`` mirrors
``automation-command.v1.json``). "Mirror" only holds if the wire contract and the
code agree in *both* directions; when they drift apart silently a payload one side
produces is rejected by the other. That is exactly how the ``player-action-request``
``parameters`` nullability mismatch slipped through a one-off manual check: the code
serialized ``"parameters": null`` while the contract typed ``parameters`` as a plain
object, so each side was internally consistent but they disagreed with each other.

These tests pin the agreement so CI, not a hand-run script, catches the next drift:

- the model's wire field names equal the schema's ``properties`` keys;
- the model's required wire fields equal the schema's ``required`` set;
- an instance the model serializes validates against the schema (serialize direction);
- a payload the schema permits parses back into the model (parse direction).
"""

import json
from datetime import datetime
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import BaseModel

from app.modules.automation.api.schemas import AutomationCommandV1, CommandSource
from app.modules.player_actions.api.schemas import PlayerActionRequestV1

_CONTRACTS = Path(__file__).resolve().parents[2] / "packages" / "contracts" / "schemas"

# One representative instance per mirror, with every optional field left at its
# default — so ``parameters`` serializes to ``null``, the exact shape the
# nullability bug produced.
_INSTANCES: dict[str, BaseModel] = {
    "player-action-request.v1.json": PlayerActionRequestV1(
        request_id="req-1",
        player_id="player-1",
        lease_id="lease-1",
        plot_id="plot-1",
        crop_cycle_id="cycle-1",
        action_type="request_extra_watering",
        requested_at=datetime(2026, 7, 22, 10, 0, 0),
    ),
    "automation-command.v1.json": AutomationCommandV1(
        command_id="cmd-1",
        plot_id="plot-1",
        actuator_id="pump-1",
        command_type="start",
        source=CommandSource.automation,
        reason="soil moisture below threshold",
        idempotency_key="key-1",
        issued_at=datetime(2026, 7, 22, 10, 0, 0),
    ),
}

MIRRORS = [
    pytest.param(
        PlayerActionRequestV1, "player-action-request.v1.json", id="player-action-request"
    ),
    pytest.param(AutomationCommandV1, "automation-command.v1.json", id="automation-command"),
]


def _load(contract_file: str) -> dict:
    return json.loads((_CONTRACTS / contract_file).read_text(encoding="utf-8"))


def _wire_schema(model: type[BaseModel]) -> dict:
    """The model's own JSON Schema in wire (camelCase alias) terms."""
    return model.model_json_schema(by_alias=True)


@pytest.mark.parametrize(("model", "contract_file"), MIRRORS)
def test_property_names_match(model: type[BaseModel], contract_file: str) -> None:
    contract = _load(contract_file)
    model_props = set(_wire_schema(model)["properties"])
    assert model_props == set(contract["properties"]), (
        f"{model.__name__} field set drifted from {contract_file}"
    )


@pytest.mark.parametrize(("model", "contract_file"), MIRRORS)
def test_required_fields_match(model: type[BaseModel], contract_file: str) -> None:
    contract = _load(contract_file)
    model_required = set(_wire_schema(model).get("required", []))
    assert model_required == set(contract.get("required", [])), (
        f"{model.__name__} required set drifted from {contract_file}"
    )


@pytest.mark.parametrize(("model", "contract_file"), MIRRORS)
def test_serialized_instance_validates_against_contract(
    model: type[BaseModel], contract_file: str
) -> None:
    """A model-produced payload (optionals at default) must satisfy the contract.

    This is the check the manual pass never ran for ``player-action-request``:
    with ``parameters`` typed ``object`` rather than ``["object", "null"]`` the
    emitted ``"parameters": null`` fails validation here.
    """
    payload = json.loads(_INSTANCES[contract_file].model_dump_json(by_alias=True))
    Draft202012Validator(_load(contract_file)).validate(payload)


@pytest.mark.parametrize(("model", "contract_file"), MIRRORS)
def test_contract_permitted_null_parameters_round_trips(
    model: type[BaseModel], contract_file: str
) -> None:
    """Parse direction: a ``parameters: null`` payload is both contract-legal and
    accepted by the code, and re-parses to ``None``. The two must agree, not merely
    each be internally consistent.
    """
    payload = json.loads(_INSTANCES[contract_file].model_dump_json(by_alias=True))
    payload["parameters"] = None
    Draft202012Validator(_load(contract_file)).validate(payload)
    assert model.model_validate(payload).parameters is None
