import csv
from typing import Any

from fastapi import Depends

from ..models.books import BookCreate
from .books import BooksService


class LoadBooksService:
    def __init__(self, books_service: BooksService = Depends()):
        self.books_service = books_service

    def import_csv(self, company_id: int, file: Any):
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=[
                "title",
                "year",
                "description",
                "image_link",
                "ISBN",
                "number_page",
                "genre",
            ],
        )
        books = []
        next(reader)
        for row in reader:
            book_data = BookCreate.parse_obj(row)
            if book_data.image_link == "":
                book_data.image_link = None
            books.append(book_data)

        self.books_service.create_many(
            company_id,
            books,
        )
