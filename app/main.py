from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from app.api.v1.router import router as v1_router
from app.api.errors import http_exception_handler, validation_exception_handler
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(
    title="Organizational Structure API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(v1_router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
