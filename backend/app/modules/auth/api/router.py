"""Auth API router — login, refresh, logout, me."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import TokenPayload, get_current_user
from app.modules.auth.application.login_handler import login_user
from app.modules.auth.application.refresh_handler import refresh_tokens

router = APIRouter(prefix="/auth", tags=["auth"])


# ── Request / Response Schemas ────────────────────────────────────────────────


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    role: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.post("/login", response_model=LoginResponse, summary="Authenticate user")
async def login(
    body: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LoginResponse:
    """
    Authenticate with email + password.
    Returns a short-lived JWT access token and a long-lived refresh token.
    """
    try:
        result = await login_user(email=body.email, password=body.password, db=db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    return LoginResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        user=UserOut(
            id=result.user.id,
            email=result.user.email,
            full_name=result.user.full_name,
            role=result.user.role,
        ),
    )


@router.post("/refresh", response_model=RefreshResponse, summary="Rotate refresh token")
async def refresh(
    body: RefreshRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RefreshResponse:
    """
    Exchange a valid refresh token for a new access token + new refresh token.
    The submitted refresh token is immediately revoked (rotation).

    This endpoint must be accessible without a JWT (AllowAnonymous equivalent).
    """
    try:
        result = await refresh_tokens(plain_token=body.refresh_token, db=db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    return RefreshResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
    )


@router.get("/me", response_model=MeResponse, summary="Get current user profile")
async def me(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MeResponse:
    """
    Return the authenticated user's profile.
    Requires a valid JWT access token.
    """
    from sqlalchemy import select

    from app.modules.auth.domain.user_model import User

    result = await db.execute(select(User).where(User.id == current_user.sub))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return MeResponse(id=user.id, email=user.email, full_name=user.full_name, role=user.role)
