from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status

from ..models.auth import Company
from ..models.books import Book, BookCreate, BookUpdate
from ..services.auth import get_current_user
from ..services.books import BooksService


router = APIRouter(
    prefix="/books"
)


@router.get("/", response_model=List[Book])
def get_book(
    genre: Optional[str] = None,
    company: Company = Depends(get_current_user),
    service: BooksService = Depends()
):
    return service.get_list(company_id=company.id, genre=genre)


@router.post("/", response_model=Book)
def create_book(
    book_data: BookCreate,
    company: Company = Depends(get_current_user),
    service: BooksService = Depends(),
):
    return service.create(company_id=company.id, book_data=book_data)


@router.get("/{book_id}", response_model=Book)
def get_book(
    book_id: int,
    company: Company = Depends(get_current_user),
    service: BooksService = Depends(),
):
    return service.get(company_id=company.id, book_id=book_id)


@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    company: Company = Depends(get_current_user),
    service: BooksService = Depends()
):
    return service.update(
        company_id=company.id,
        book_id=book_id,
        book_data=book_data
    )


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    company: Company = Depends(get_current_user),
    service: BooksService = Depends()
):
    service.delete(company_id=company.id, book_id=book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
