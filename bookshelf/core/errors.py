from werkzeug.exceptions import HTTPException

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .extensions import AppError


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def _validation(request: Request, exc: RequestValidationError):
        _details = [
            {"field": ".".join(str(p) for p in err["loc"][1:]), "message": err["msg"]}
            for err in exc.errors()
        ]
        return _error(400, "validation_error", "Request is invalid", details=_details)
    
    @app.exception_handler(AppError)
    async def _app_error(request: Request, exc: AppError):
        return _error(exc.status_code, exc.code, exc.message, exc.details)

    @app.exception_handler(IntegrityError)
    async def _integrity(request: Request, exc: IntegrityError):
        return _error(409, "conflict", "Resource violates a uniqueness or integrity rule")

    @app.exception_handler(StarletteHTTPException)       # Starlette's, so unknown routes are caught too
    async def _http(request: Request, exc: StarletteHTTPException):
        return _error(exc.status_code, "http_error", str(exc.detail))

    @app.exception_handler(Exception)
    async def _unexpected(request: Request, exc: Exception):
        return _error(500, "internal_error", "Unexpected error")

    
def _error(status: int, code: str, message: str, details=None):
    body = { "error": { "code": code, "message": message, "details": details or [] } }
    return JSONResponse(status_code=status, content=body)
