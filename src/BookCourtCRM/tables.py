import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    author = sa.Column(sa.String)
    year = sa.Column(sa.String)
    isbn = sa.Column(sa.String)
    genre = sa.Column(sa.String)

    # book_cover = sa.Column(sa.string)
    # description = sa.Column(sa.string)
    # site_link = sa.Column(sa.string)
    # company_id = sa.Column(sa.Integer)


class Company(Base):
    __tablename__ = "companies"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    address = sa.Column(sa.String)
    representative_name = sa.Column(sa.String)
    representative_job_title = sa.Column(sa.String)
    company_site = sa.Column(sa.String)
    company_mail = sa.Column(sa.String)
    company_phone = sa.Column(sa.String)
    company_info = sa.Column(sa.String)


