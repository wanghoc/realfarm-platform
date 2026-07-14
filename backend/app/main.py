"""
RealFarm API — FastAPI application entry point.

Starts the modular monolith. Each module registers its own router.
Modules communicate through application interfaces, not direct ORM coupling.
"""

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import AsyncSessionFactory, Base, engine
from app.core.logging import configure_logging
from app.modules.admin.api.router import router as admin_router

# Module routers
from app.modules.auth.api.router import router as auth_router
from app.modules.auth.domain.refresh_token_model import RefreshToken  # noqa: F401

# Import all ORM models so that Base.metadata knows about them
# before create_all / Alembic runs.
from app.modules.auth.domain.user_model import User  # noqa: F401
from app.modules.automation.api.router import router as automation_router
from app.modules.care_logs.api.router import router as care_logs_router
from app.modules.crop_catalog.api.router import router as crop_catalog_router
from app.modules.crop_cycles.api.router import router as crop_cycles_router
from app.modules.deliveries.api.router import router as deliveries_router
from app.modules.farms.api.router import router as farms_router
from app.modules.harvests.api.router import router as harvests_router
from app.modules.incidents.api.router import router as incidents_router
from app.modules.leases.api.router import router as leases_router
from app.modules.notifications.api.router import router as notifications_router
from app.modules.player_actions.api.router import router as player_actions_router
from app.modules.plots.api.router import router as plots_router
from app.modules.telemetry.api.router import router as telemetry_router
from app.modules.traceability.api.router import router as traceability_router
from app.modules.users.api.router import router as users_router
from app.modules.work_orders.api.router import router as work_orders_router

configure_logging()
log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: create tables (use Alembic in production) and seed demo data.
    Shutdown: nothing special required.
    """
    log.info("realfarm.api.startup", env=settings.APP_ENV)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed demo user in development only
    if settings.APP_ENV == "development":
        from app.modules.auth.application.seeder import seed_demo_user

        async with AsyncSessionFactory() as session, session.begin():
            await seed_demo_user(session)
        log.info("realfarm.api.seeded_demo_user")

    yield
    log.info("realfarm.api.shutdown")


app = FastAPI(
    title="RealFarm API",
    version="0.1.0",
    description=(
        "Backend for the RealFarm remote farming experience platform. "
        "See /api/docs for interactive documentation."
    ),
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# CORS — allow Vite dev server and configured web origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.WEB_BASE_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register module routers ──────────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(farms_router, prefix=API_PREFIX)
app.include_router(plots_router, prefix=API_PREFIX)
app.include_router(crop_catalog_router, prefix=API_PREFIX)
app.include_router(leases_router, prefix=API_PREFIX)
app.include_router(crop_cycles_router, prefix=API_PREFIX)
app.include_router(telemetry_router, prefix=API_PREFIX)
app.include_router(automation_router, prefix=API_PREFIX)
app.include_router(player_actions_router, prefix=API_PREFIX)
app.include_router(work_orders_router, prefix=API_PREFIX)
app.include_router(care_logs_router, prefix=API_PREFIX)
app.include_router(incidents_router, prefix=API_PREFIX)
app.include_router(harvests_router, prefix=API_PREFIX)
app.include_router(deliveries_router, prefix=API_PREFIX)
app.include_router(notifications_router, prefix=API_PREFIX)
app.include_router(traceability_router, prefix=API_PREFIX)
app.include_router(admin_router, prefix=API_PREFIX)


@app.get("/health", tags=["health"], summary="Liveness probe")
async def health_check() -> dict:
    return {"status": "ok", "version": app.version}
