from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])

class Book(models.Model):
    book_name = models.CharField(max_length = 200)
    book_price = models.IntegerField(default = 0)
    available = models.BooleanField()
    isbn = models.CharField(max_length = 20)
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.book_name





