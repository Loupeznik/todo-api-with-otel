import json
import logging

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from alembic import command
from alembic.config import Config
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.instrumentation import setup_instrumentation

logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_instrumentation()
    logger.info("Application startup complete")
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Alembic migrations
alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc: StarletteHTTPException):
    if exc.status_code != 500:
        return await http_exception_handler(request, exc)
    else:
        logger.error(exc.detail)

        return JSONResponse(
            status_code=exc.status_code,
            content={"message": "An error has occured"}
        )

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

FastAPIInstrumentor.instrument_app(app)

app.include_router(api_router, prefix=settings.API_V1_STR)
