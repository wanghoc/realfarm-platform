"""Traceability module router.

Provides complete off-chain timelines and QR-accessible read-only views.
Only hashes and minimal metadata may be anchored on-chain.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/traceability", tags=["traceability"])


@router.get("/crop-cycles/{cycle_id}/timeline")
async def get_traceability_timeline(
    cycle_id: str,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> dict:
    """Return the full traceability timeline for a crop cycle. TODO: implement."""
    return {"cycle_id": cycle_id, "events": []}


@router.get("/qr/{token}")
async def get_public_qr_view(token: str) -> dict:
    """Public QR-accessible read-only traceability view (no auth required). TODO: implement."""
    return {"token": token, "events": []}
