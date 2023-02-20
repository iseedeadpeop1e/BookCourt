from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.books import Book, BookCreate


class BookService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self, author: Optional[str] = None) -> List[tables.Book]:
        query = self.session.query(tables.Book)
        if author:
            query = query.filter_by(author=author)
        books = query.all()
        return books

    def create(self, operation_data: BookCreate) -> tables.Book:
        book = tables.Book(**operation_data.dict())
        self.session.add(book)
        self.session.commit()
        return book
