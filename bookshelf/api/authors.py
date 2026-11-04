from flask import Blueprint, jsonify, request
from ..schemas.author import AuthorCreate, AuthorDetailOut, AuthorOut
from ..services.author_service import AuthorService

authors_bp = Blueprint("authors", __name__, url_prefix="/api/v1/authors")

@authors_bp.get("/<int:author_id>")
def get_author_by_id(author_id: int):
    author = AuthorService().get(author_id, with_books=True)
    return jsonify(AuthorDetailOut.model_validate(author).model_dump(mode="json"))

@authors_bp.post("")
def create_author():
    data = AuthorCreate.model_validate(request.get_json(silent=True) or {})
    author = AuthorService().create(**data.model_dump())
    return jsonify(AuthorOut.model_validate(author).model_dump(mode="json")), 201

@authors_bp.delete("/<int:author_id>")
def delete_author(author_id: int):
    AuthorService().delete(author_id)
    return "", 204