from django.test import TestCase
from libraryapp.models import *

# Create your tests here.

class AuthorTestCase(TestCase):

    def setUp(self):
        """only add data in your virtual database"""
        Author.objects.create(first_name = 'John', last_name = 'Doe')

    def test_case_check_author_fullname(self):
        """get the object from virtual database and assert equal"""
        author = Author.objects.get(first_name='John', last_name='Doe')
        self.assertEqual(author.fullname(), 'John Doe')

class RecordTestCase(TestCase):
    def setUp(self):
        author = Author.objects.create(first_name = 'John', last_name = 'Doe')
        Book.objects.create(book_name = 'Rambo', book_price= 300, isbn= '983-2379-327-1-71', stock= 3, author = author)
        Member.objects.create(member_name = 'Sachin', member_phone = 9876543210, member_address = 'Trivandrum')

    def test_case_check_stock_update(self):
        book = Book.objects.get(book_name = 'Rambo')
        member = Member.objects.get(member_name = 'Sachin')
        initial_stock = book.stock
        Record.objects.create(book = book, borrower_name = member)
        final_stock = book.stock
        self.assertEqual(initial_stock-final_stock , 1)

