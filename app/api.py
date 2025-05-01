from ninja import NinjaAPI, Schema
from .models import Book, Author
from django.shortcuts import get_object_or_404
from .schemas import BookSchema, CreateBookSchema, AuthorSchema, CreateAuthorSchema, AuthorSearchSchema, BookSearchSchema
from typing import List, Optional
from django.db.models import Count
from datetime import date

api = NinjaAPI()

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

# Book Endpoints

@api.get('/books', response=list[BookSchema])
def list_books(request):
    """
    Retrieve all books with their author details.
    Returns a list of books with nested author information.
    """
    books = Book.objects.select_related('author').all()
    return books

@api.post('/books', response=BookSchema)
def create_book(request, payload: CreateBookSchema):
    """
    Create a new book.
    Requires title, author_id, published_date, and isbn.
    Returns the created book with author details.
    """
    book = Book.objects.create(
        title=payload.title,
        author_id=payload.author_id,
        published_date=payload.published_date,
        isbn=payload.isbn
    )
    return book

@api.get('/books/{book_id}', response=BookSchema)
def get_book(request, book_id: int):
    """
    Retrieve a specific book by its ID.
    Returns the book with its author details.
    Returns 404 if book not found.
    """
    book = get_object_or_404(Book.objects.select_related('author'), id=book_id)
    return book

@api.put('/books/{book_id}', response=BookSchema)
def update_book(request, book_id: int, payload: CreateBookSchema):
    """
    Update an existing book.
    Can update title, author_id, published_date, and isbn.
    Returns the updated book with author details.
    Returns 404 if book not found.
    """
    book = get_object_or_404(Book, id=book_id)
    for attr, value in payload.dict().items():
        if attr == 'author_id':
            book.author_id = value
        else:
            setattr(book, attr, value)
    book.save()
    return book

@api.delete('/books/{book_id}')
def delete_book(request, book_id: int):
    """
    Delete a book by its ID.
    Returns success message.
    Returns 404 if book not found.
    """
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {'message': 'Book deleted successfully ! '}

# Author Endpoints

@api.get('/authors', response=list[AuthorSchema])
def list_authors(request):
    """
    Retrieve all authors.
    Returns a list of authors with their details.
    """
    authors = Author.objects.all()
    return authors

@api.get('/authors/{author_id}', response=AuthorSchema)
def get_author(request, author_id: int):
    """
    Retrieve a specific author by ID.
    Returns author details.
    Returns 404 if author not found.
    """
    authors = get_object_or_404(Author, id=author_id)
    return authors

@api.post('/authors', response=AuthorSchema)
def create_author(request, payload: CreateAuthorSchema):
    """
    Create a new author.
    Requires name, optional biography, birth_date, and nationality.
    Returns the created author details.
    """
    author = Author.objects.create(**payload.dict())
    return author

@api.put('/authors/{author_id}', response=AuthorSchema)
def update_author(request, author_id: int, payload: CreateAuthorSchema):
    """
    Update an existing author.
    Can update name, biography, birth_date, and nationality.
    Returns the updated author details.
    Returns 404 if author not found.
    """
    author = get_object_or_404(Author, id=author_id)
    for key, value in payload.dict().items():
        setattr(author, key, value)
    author.save()
    return author

@api.delete('/authors/{author_id}')
def delete_author(request, author_id: int):
    """
    Delete an author by ID.
    Returns success message.
    Returns 404 if author not found.
    """
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return {'message': 'Author deleted successfully ! '}

@api.get('/authors/{author_id}/books', response=list[BookSchema])
def get_author_books(request, author_id: int):
    """
    Retrieve all books written by a specific author.
    Returns list of books with author details.
    Returns 404 if author not found.
    """
    author = get_object_or_404(Author, id=author_id)
    return author.books.all()

# Search and Filter Endpoints

@api.get('/authors/search', response=list[AuthorSchema])
def search_authors(request, payload: AuthorSearchSchema):
    """
    Search authors by name and/or nationality.
    Returns filtered list of authors matching the criteria.
    """
    authors = Author.objects.all()
    if payload.name:
        authors = authors.filter(name__icontains=payload.name)
    if payload.nationality:
        authors = authors.filter(nationality__icontains=payload.nationality)
    return authors

@api.get('/books/search', response=list[BookSchema])
def search_books(request, payload: BookSearchSchema):
    """
    Search books by title, date range, and/or author.
    Returns filtered list of books matching the criteria.
    """
    books = Book.objects.all()
    if payload.title: 
        books = books.filter(title__icontains=payload.title)
    if payload.start_date:
        books = books.filter(published_date__gte=payload.start_date)
    if payload.end_date:
        books = books.filter(published_date__lte=payload.end_date)
    if payload.author_id:
        books = books.filter(author_id=payload.author_id)
    return books