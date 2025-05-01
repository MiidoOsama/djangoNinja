from ninja import Schema
from typing import Optional, List
from datetime import date

class AuthorSchema(Schema):
    id: str
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None

class AuthorCreateSchema(Schema):
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None

class BookSchema(Schema):
    id: str
    title: str
    author_id: str
    published_date: date
    isbn: str

class BookCreateSchema(Schema):
    title: str
    author_id: str
    published_date: date
    isbn: str

class AuthorSearchSchema(Schema):
    name: Optional[str] = None
    nationality: Optional[str] = None

class BookSearchSchema(Schema):
    title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    author_id: Optional[int] = None