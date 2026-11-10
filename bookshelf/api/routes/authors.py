from fastapi import APIRouter, Request, Response
from ...schemas.author import AuthorCreate, AuthorDetailOut, AuthorOut
from ...services.author_service import AuthorService

router = APIRouter(tags=["authors"], prefix="/api/v1/authors")

@router.get("/{author_id}", response_model=AuthorDetailOut)
async def get_author_by_id(author_id: int):
    author = await AuthorService().get(author_id, with_books=True)
    return AuthorDetailOut.model_validate(author).model_dump(mode="json")

@router.post("", response_model=AuthorOut, status_code=201)
async def create_author(body: AuthorCreate, service: AuthorService, request: Request, response: Response):
    author = await service.create(**body.model_dump())
    return AuthorOut.model_validate(author).model_dump(mode="json")

@router.delete("/{author_id}", status_code=204)
async def delete_author(author_id: int):
    await AuthorService().delete(author_id)