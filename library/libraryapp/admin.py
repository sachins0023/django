from django.contrib import admin

# Register your models here.
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'book_price', 'available', 'isbn', 'author', 'stock',)
    ordering = ('book_name',)
    list_filter = ('available',)
    search_fields = ['book_name', 'isbn',]
    # fields = ('book_name', 'isbn', 'book_price')

admin.site.register(Book, BookAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    ordering = ('first_name', )

admin.site.register(Author, AuthorAdmin)


class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'member_phone', 'member_address')

admin.site.register(Member, MemberAdmin)

class RecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrow_date', 'return_date', 'borrower_name', 'returned')

admin.site.register(Record, RecordAdmin)