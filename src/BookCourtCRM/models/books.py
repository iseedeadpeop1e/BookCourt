
from pydantic import BaseModel


class BookBase(BaseModel):
    name: str
    author: str
    year: str
    isbn: str
    genre: str


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    pass
