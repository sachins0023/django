from django.contrib import admin
from django import forms

# Register your models here.
from .models import *

class BookAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookAdminForm,self).__init__(*args, **kwargs)

    def clean(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) < 4:
            raise forms.ValidationError("ISBN should not be less than 4 characters", code = 'invalid')
        return self.cleaned_data

    def save(self, commit = True):
        return super(BookAdminForm, self).save(commit = commit)

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'book_price', 'available', 'isbn', 'author', 'stock',)
    ordering = ('book_name',)
    list_filter = ('available',)
    search_fields = ['book_name', 'isbn',]
    form = BookAdminForm
    # fields = ('book_name', 'isbn', 'book_price')

admin.site.register(Book, BookAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    ordering = ('first_name', )

admin.site.register(Author, AuthorAdmin)


class MemberAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemberAdminForm,self).__init__(*args, **kwargs)

    def clean(self):
        phone = self.cleaned_data.get('member_phone')
        if phone != None:
            if len(str(phone)) != 10:
                raise forms.ValidationError("Enter a valid phone number (10 digit number)", code = 'invalid')
        return self.cleaned_data

    def save(self, commit = True):
        return super(MemberAdminForm, self).save(commit = commit)


class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'member_phone', 'member_address')
    form = MemberAdminForm

admin.site.register(Member, MemberAdmin)


class RecordAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecordAdminForm,self).__init__(*args, **kwargs)

    def clean(self):
        book_name = self.cleaned_data.get('book')
        if book_name.stock == 0:
            if self.cleaned_data.get('returned') == False:
                raise forms.ValidationError("Book out of stock!", code = 'invalid')
        return self.cleaned_data

    def save(self, commit = True):
        return super(RecordAdminForm, self).save(commit = commit)

class RecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrow_date', 'return_date', 'borrower_name', 'returned')
    form = RecordAdminForm

admin.site.register(Record, RecordAdmin)