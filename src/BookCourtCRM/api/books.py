from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends

from ..models.books import Book, BookCreate
from ..services.books import BookService


router = APIRouter(
    prefix="/catalog"
)


@router.get("/", response_model=List[Book])
def get_books(
     author: Optional[str] = None,
     service: BookService = Depends()
):
    return service.get_list(author=author)


@router.post("/", response_model=Book)
def create_book(
    operation_data: BookCreate,
    service: BookService = Depends(),
):
    return service.create(operation_data)
