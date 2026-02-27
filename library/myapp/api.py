from datetime import date
from typing import List
from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from .models import Author, Book
from ninja import FilterSchema, FilterLookup
from typing import Annotated, Optional
from ninja import Query

api = NinjaAPI()


class AuthorIn(Schema):
    first_name: str
    last_name: str
    patronymic: str
    birthdate: date = None

class AuthorOut(Schema):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    birthdate: date = None

class BookIn(Schema):
    title: str
    authors: List[int]
    description: str = ""

class BookOut(Schema):
    id: int
    title: str
    description: str
    authors: List[AuthorOut]
    
class BookFilterSchema(FilterSchema):
    name: Annotated[Optional[str], FilterLookup("title__icontains")] = None


@api.post("/authors")
def create_author(request, payload: AuthorIn):
    author = Author.objects.create(**payload.dict())
    return {"id": author.id}

@api.get("/authors/{author_id}", response=AuthorOut)
def get_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    return author

@api.get("/authors", response=List[AuthorOut])
def list_authors(request):
    return Author.objects.all()

@api.put("/authors/{author_id}")
def update_author(request, author_id: int, payload: AuthorIn):
    author = get_object_or_404(Author, id=author_id)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return {"success": True}

@api.delete("/authors/{author_id}")
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return {"success": True}

@api.post("/books")
def create_book(request, payload: BookIn):
    authors_ids = payload.authors
    book = Book.objects.create(
        title=payload.title,
        description=payload.description
    )
    book.authors.set(authors_ids)
    return {"id": book.id}

@api.get("/books/{book_id}", response=BookOut)
def get_book(request, book_id: int):
    return get_object_or_404(Book, id=book_id)


@api.get("/books", response=List[BookOut])
def list_books(request, filters: Query[BookFilterSchema]):
    books = Book.objects.prefetch_related("authors").all()
    return filters.filter(books)


@api.put("/books/{book_id}")
def update_book(request, book_id: int, payload: BookIn):
    book = get_object_or_404(Book, id=book_id)
    book.title = payload.title
    book.description = payload.description
    book.save()
    book.authors.set(payload.authors)
    return {"success": True}


@api.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}