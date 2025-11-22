"""
Lyra Agent Server

FastAPI application factory and server configuration.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import get_settings
from app.routes import core, memory, congress


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler for startup and shutdown events.
    """
    settings = get_settings()
    logger.info(f"Starting {settings.AGENT_NAME} agent v{settings.VERSION}")
    logger.info(f"Memory directory: {settings.MEMORY_DIR}")
    logger.info(f"RAG directory: {settings.RAG_DIR}")

    # Startup: Initialize resources
    yield

    # Shutdown: Cleanup resources
    logger.info(f"Shutting down {settings.AGENT_NAME} agent")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    settings = get_settings()

    app = FastAPI(
        title=f"{settings.AGENT_NAME} Agent",
        description="Lyra - Creative strategist and conceptual reframing agent",
        version=settings.VERSION,
        lifespan=lifespan,
    )

    # Minimal CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(core.router, tags=["core"])
    app.include_router(memory.router)  # Phase 4: Memory endpoints
    app.include_router(congress.router)  # Phase 5: Congress endpoints

    return app


# Create the application instance
app = create_app()
