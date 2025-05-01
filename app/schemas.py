from ninja import Schema 
from datetime import date 
from typing import Optional
from django.db.models import Count

class AuthorSchema(Schema):
    id: int 
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None

class CreateAuthorSchema(Schema):
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None

class BookSchema(Schema):
    id : int
    title : str 
    author : AuthorSchema
    published_date : date
    isbn : str

class CreateBookSchema(Schema):
    title : str 
    author_id : int
    published_date : date
    isbn : str

class AuthorSearchSchema(Schema):
    name: Optional[str] = None
    nationality: Optional[str] = None

class BookSearchSchema(Schema):
    title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    author_id: Optional[int] = None