from django.db import models

# Create your models here.

class Library(models.Model):
    name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 50)
    email = models.EmailField(blank = True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Library"
        verbose_name_plural = "Libraries"

class Librarian(models.Model):
    first_name = models.CharField(max_length = 50)
    middle_name= models.CharField(null = True, blank = True, max_length=50)
    last_name = models.CharField(max_length = 50)
    library = models.ForeignKey(Library, on_delete = models.CASCADE)
    contact_number = models.CharField(blank = True, null = True, max_length = 10)

    def fullname(self):
        if self.middle_name is None:
            return "{} {}".format(self.first_name,self.last_name)
        else:
            return "{} {} {}".format(self.first_name,self.middle_name,self.last_name)

    def __str__(self):
        return self.fullname()

class Book(models.Model):
    book_name = models.CharField(max_length = 50)
