from werkzeug.exceptions import HTTPException

from flask import jsonify
from psycopg import IntegrityError
from pydantic import ValidationError


class AppError(Exception):
    status_code = 500
    code = "internal_error"

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

class NotFoundError(AppError):
    status_code = 404
    code = "not_found"

class ConflictError(AppError):
    status_code = 409
    code = "conflict"

class BusinessRuleError(AppError):
    status_code = 422
    code = "business_rule_violation"

def _error(status: int, code: str, message: str, details=None):
    body = { "error": { "code": code, "message": message, "details": details or [] } }
    return jsonify(body), status


def register_error_handlers(app) -> None:
    from .extensions import db

    @app.errorhandler(ValidationError)
    def _validation(exc: ValidationError):
        details = [
            {"field": ".".join(str(p) for p in err["loc"]), "message": err["msg"]}
            for err in exc.errors()
        ]
        return _error(400, "validation_error", "Request body is invalid", details)

    @app.errorhandler(AppError)
    def _app_error(err: AppError):
        db.session.rollback()
        return _error(err.status_code, err.code, err.message, err.details)

    @app.errorhandler(IntegrityError)
    def _integrity(exc: IntegrityError):
        db.session.rollback()
        return _error(409, "conflict", "Resource violates a uniqueness or integrity rule")

    @app.errorhandler(HTTPException)
    def _http(exc: HTTPException):
        return _error(exc.code or 500, "http_error", exc.description)

    @app.errorhandler(Exception)
    def _unexpected(exc: Exception):
        db.session.rollback()
        app.logger.exception("Unhandled error")
        return _error(500, "internal_error", "Unexpected error")