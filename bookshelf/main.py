from contextlib import asynccontextmanager

from fastapi import FastAPI
from .api.routes import health, books, authors
from .core.database import engine
from .core.errors import register_error_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title="Bookshelf API", version="1.0.0" lifespan=lifespan)
    register_error_handlers(app)

    for router in (health.router, books.router, authors.router):
        app.include_router(router)

    return app

app = create_app()

