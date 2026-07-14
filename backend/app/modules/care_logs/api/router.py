"""Care logs module router."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/care-logs", tags=["care-logs"])


@router.get("/plots/{plot_id}")
async def get_care_logs(
    plot_id: str, current_user: Annotated[TokenPayload, Depends(get_current_user)]
) -> list:
    """Get care log history for a plot. TODO: implement."""
    return []
