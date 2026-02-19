from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100) 
    patronymic = models.CharField(max_length=100) 
    birthdate =  models.DateField(null=True, blank=True)
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, related_name="books")
    description = models.TextField(blank=True)