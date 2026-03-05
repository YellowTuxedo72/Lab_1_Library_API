from datetime import date
from typing import List
from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from .models import Author, Book
from ninja import FilterSchema, FilterLookup
from typing import Annotated, Optional
from ninja import Query
from ninja import File, UploadedFile

api = NinjaAPI()

class BookIn(Schema):
    title: str
    description: str = None
    year_of_publishing: date
    number_of_pages: int
    author_id: int
    
class AuthorOut(Schema):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    birthdate: date = None
    
class AuthorIn(Schema):
    first_name: str
    last_name: str
    patronymic: str
    birthdate: date
    
class BookOut(Schema):
    id: int
    title: str
    description: str = None
    year_of_publishing: date
    number_of_pages: int
    image: str = None
    author: AuthorOut
    
class BookFilterSchema(FilterSchema):
    title: Annotated[Optional[str], FilterLookup("title__icontains")] = None
    author: Annotated[Optional[str], FilterLookup(["author__first_name__icontains", "author__last_name__icontains", "author__patronymic__icontains"])] = None
    
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
    qs = Author.objects.all()
    return qs

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
def create_book(request, payload: BookIn, image: File[UploadedFile] = None):
    data = payload.dict()
    author_id = data.pop("author_id")
    book = Book.objects.create(author_id=author_id, **data)
    if image:
        book.image.save(image.name, image)

    return {"id": book.id}

@api.get("/books/{book_id}", response=BookOut)
def get_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    return book

@api.get("/books", response=List[BookOut])
def list_books(request):
    return Book.objects.all()

@api.put("/books/{book_id}")
def update_book(request, book_id: int, payload: BookIn):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return {"success": True}

@api.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}