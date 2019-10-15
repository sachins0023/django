from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

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
    stock = models.IntegerField(null = True, default = 1)

    def __str__(self):
        return self.book_name

class Member(models.Model):
    member_name = models.CharField(null = True, blank = True, max_length = 50)
    member_phone = models.IntegerField(null = True, blank = True)
    member_address = models.CharField(null = True, blank = True, max_length = 200)

    def __str__(self):
        return self.member_name

class Record(models.Model):
    book = models.ForeignKey(Book, null = True, on_delete = models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField()
    borrower_name = models.ForeignKey(Member, on_delete = models.CASCADE)
    #returned_check = models.BooleanField(default = False)
    returned = models.BooleanField(default = False)
    def __str__(self):
        return self.book.book_name

@receiver(pre_save, sender = Book)
def assign_available(sender, instance, **kwargs):
    book = instance
    if book.stock == 0:
        book.available = True
    else:
        book.available = False
    book.save()




@receiver(pre_save, sender = Record)
def increment_stock(sender, instance, **kwargs):
    if instance.returned == False:
        if any(Record.objects.filter(id=instance.id)):
            if Record.objects.get(id=instance.id).returned == True:
                instance.returned = True
    else:
        if Record.objects.get(id=instance.id).returned == False:
            book = instance.book
            book.stock = book.stock + 1
            if book.stock > 0:
                book.available = True
            book.save()

@receiver(post_save, sender = Record)
def decrement_stock(sender, instance, created, **kwargs):
    if created:
        book = instance.book
        if book.available == True:
            book.stock = book.stock - 1
            if book.stock < 1:
                book.available = False
            book.save()