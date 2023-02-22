import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id = sa.Column(sa.Integer, primary_key=True)
    company_name = sa.Column(sa.String, unique=True)
    email = sa.Column(sa.String, unique=True)
    phone_number = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean)
    address = sa.Column(sa.String)
    created_at = sa.Column(sa.Integer)
    password_hash = sa.Column(sa.Text)

    # representative_name = sa.Column(sa.String)
    # representative_job_title = sa.Column(sa.String)
    # company_site = sa.Column(sa.String)
    # company_info = sa.Column(sa.String)


class Book(Base):
    __tablename__ = "books"

    id = sa.Column(sa.Integer, primary_key=True)
    company_id = sa.Column(sa.Integer, sa.ForeignKey("companies.id"))
    title = sa.Column(sa.String)
    year = sa.Column(sa.Integer)
    description = sa.Column(sa.String)
    image_link = sa.Column(sa.String)
    ISBN = sa.Column(sa.String)
    number_page = sa.Column(sa.String)
    genre = sa.Column(sa.String)

    # author = sa.Column(sa.String)
    # site_link = sa.Column(sa.String)
    # company_id = sa.Column(sa.Integer)


