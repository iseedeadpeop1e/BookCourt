from typing import List, Optional

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.books import Book, BookCreate, BookUpdate


class BooksService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self, company_id: int, genre: Optional[str] = None) -> List[tables.Book]:
        query = (
            self.session
            .query(tables.Book)
            .filter_by(company_id=company_id)
        )
        if genre:
            query = query.filter_by(genre=genre)
        books = query.all()
        return books

    def _get(self, company_id: int, book_id: int) -> tables.Book:
        book = (
            self.session
            .query(tables.Book)
            .filter_by(
                id=book_id,
                company_id=company_id,
            )
            .first()
        )
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return book

    def get(self, company_id: int, book_id: int) -> tables.Book:
        return self._get(company_id, book_id)

    def create_many(self, company_id: int, book_data: List[BookCreate]) -> List[tables.Book]:
        books = [
            tables.Book(
                **book_data.dict(),
                company_id=company_id,
            )
            for book_data in book_data
        ]
        self.session.add_all(books)
        self.session.commit()
        return books

    def create(self, company_id: int, book_data: BookCreate) -> tables.Book:
        book = tables.Book(
            **book_data.dict(),
            company_id=company_id,
        )
        self.session.add(book)
        self.session.commit()
        return book

    def update(self, company_id: int, book_id: int, book_data: BookUpdate) -> tables.Book:
        book = self._get(company_id, book_id)
        for field, value in book_data:
            setattr(book, field, value)
        self.session.commit()
        return book

    def delete(self, company_id: int, book_id: int):
        book = self._get(company_id, book_id)
        self.session.delete(book)
        self.session.commit()
