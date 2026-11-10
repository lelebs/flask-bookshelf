from fastapi import APIRouter

from ...models.price_range import PriceRange

from ...services.book_service import BookService
from ...schemas.book import BookOut, BookCreate, BookUpdate, DiscountIn


router = APIRouter(tags=["books"], prefix="/api/v1/books")

@router.get("", response_model=BookPage)
async def list_books():
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 10, type=int)
    items, total = BookService().list_page(page, size)

    return jsonify(items=[_out(b) for b in items], page=page, size=size, total=total)


@books_bp.get("/<int:book_id>")
def get_book_by_id(book_id: int):
    return jsonify(_out(BookService().get(book_id)))

@books_bp.post("")
def create_book():
    data = BookCreate.model_validate(_body())
    book = BookService().create(**data.model_dump())
    location = url_for("books.get_book_by_id", book_id=book.id)

    return jsonify(_out(book)), 201, {"Location": location}

@books_bp.patch("/<int:book_id>")
def update_book(book_id: int):
    data = BookUpdate.model_validate(_body())
    changes = data.model_dump(exclude_unset=True, exclude_none=True)

    return jsonify(_out(BookService().update(book_id, **changes)))


@books_bp.delete("/<int:book_id>")
def delete_book(book_id: int):
    BookService().delete(book_id)
    return "", 204


@books_bp.post("/<int:book_id>/discount")
def change_discount(book_id: int):
    body = DiscountIn.model_validate(_body())
    return jsonify(_out(BookService().apply_discount(book_id, body.percent)))

@books_bp.get("search")
def search():
    price = PriceRange.model_validate(request.args.to_dict())
    return BookService().query_by_price_range(price.min_price, price.max_price)