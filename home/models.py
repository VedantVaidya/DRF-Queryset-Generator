from django.db import models


'''

class Author(models.Model):
    name=models.CharField(max_length=5)
    age=models.IntegerField()

class Book(models.Model):
    title=models.CharField(max_length=5)
    writer=models.ForeignKey(Author,on_delete=models.CASCADE)
    pages=models.IntegerField()


'''