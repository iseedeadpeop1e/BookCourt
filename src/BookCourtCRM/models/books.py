
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    year: str
    description: str
    image_link: str
    ISBN: str
    number_page: str
    genre: str


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass
