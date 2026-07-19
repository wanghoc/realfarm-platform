"""Shared Pydantic base for models that speak a camelCase wire contract.

Python fields stay snake_case; the wire uses camelCase aliases, so renaming a Python
field never changes the contract. ``extra="forbid"`` mirrors a contract's
``additionalProperties: false``.
"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Base model whose fields parse and serialize as camelCase on the wire."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )
