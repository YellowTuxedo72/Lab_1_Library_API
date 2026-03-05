from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100) 
    patronymic = models.CharField(max_length=100) 
    birthdate =  models.DateField(null=True, blank=True)
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="books/", null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    description = models.TextField(blank=True)
    year_of_publishing = models.DateField()
    number_of_pages = models.IntegerField()