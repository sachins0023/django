from django.db import models
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
# Create your models here.

class Library(models.Model):
    name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 50)
    email = models.EmailField(blank = True)
    membership_fee = models.FloatField(null = True)
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
    book_name = models.CharField(max_length = 100)
    author_name = models.CharField(max_length = 50, null = True, blank = True)
    publication = models.CharField(max_length = 50)
    library = models.ForeignKey(Library, on_delete = models.CASCADE)
    price = models.FloatField(null = True)
    isbn = models.CharField(null = True, max_length = 26)
    total_stock = models.IntegerField(default = 1)
    available_stock = models.IntegerField(default = 1)
    available = models.BooleanField(default = True)

    def __str__(self):
        return self.book_name




class Member(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(null=True, blank=True, max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(null = True, blank = True, max_length = 200)
    contact_number = models.CharField(null=True, blank = True, max_length=10)
    membership = models.ForeignKey(Library, on_delete=models.CASCADE)
    book_count = 4

    def fullname(self):
        if self.middle_name is None:
            return "{} {}".format(self.first_name,self.last_name)
        else:
            return "{} {} {}".format(self.first_name,self.middle_name,self.last_name)

    def __str__(self):
        return self.fullname()



class IssueRecord(models.Model):
    book_borrowed = models.ForeignKey(Book, on_delete = models.CASCADE)
    issued_librarian = models.ForeignKey(Librarian, on_delete = models.CASCADE)
    date_of_issue = models.DateField(default = datetime.now())
    date_of_return = models.DateField(default = datetime.now() + timedelta(days= 7))
    date_returned = models.DateField(null = True, blank = True)
    member = models.ForeignKey(Member, on_delete = models.CASCADE)
    returned = models.BooleanField(default = False)
    penalty_per_day = models.FloatField(default = 0)
    # len(IssueRecord.objects.get(member= 'member'))<=4
    def __str__(self):
        return self.book_borrowed.book_name

    def fine_imposed(self):
        if self.date_returned is not None:
            delta = self.date_returned - self.date_of_return
            number_of_days = delta.days
            if number_of_days>0:
                return self.penalty_per_day*number_of_days
            else:
                return 0.0


@receiver(post_save, sender = IssueRecord)
def decrement_stock(sender, instance, created, **kwargs):
    if created == True:
        book = instance.book_borrowed
        if book.available == True:
            book.available_stock = book.available_stock - 1
            if book.available_stock < 1:
                book.available = False
            book.save()

@receiver(pre_save, sender = IssueRecord)
def increment_stock(sender, instance, **kwargs):
    if instance.returned == False:
        if any(IssueRecord.objects.filter(id = instance.id)) == True:
            if IssueRecord.objects.get(id = instance.id).returned == True:
                instance.returned = True
    else:
        if IssueRecord.objects.get(id = instance.id).returned == False:
            book = instance.book_borrowed
            book.available_stock = book.available_stock + 1
            if book.available_stock>0:
                book.available = True
            book.save()

@receiver(post_save, sender = IssueRecord)
def decrement_book_count(sender, instance, **kwargs):
    member = instance.member
    member.book_count = member.book_count - 1
    member.save()

@receiver(pre_save, sender = IssueRecord)
def increment_book_count(sender, instance, **kwargs):
    if instance.returned == True:
        if IssueRecord.objects.get(id=instance.id).returned == False:
            member = instance.member
            member.book_count = member.book_count + 1
            member.save()
