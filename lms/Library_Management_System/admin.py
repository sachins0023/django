from django.contrib import admin
from Library_Management_System.models import *
from django import forms
import re

# Register your models here.

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'email',)
    ordering = ('name',)
    search_fields = ['name', 'city',]

admin.site.register(Library, LibraryAdmin)

class LibrarianAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LibrarianAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number is not None:
            regex = r"^(\d{10})$"
            match = re.search(regex, contact_number)
            if match is None:
                raise forms.ValidationError("Contact number should be 10 digits", code = 'invalid')
        return self.cleaned_data

    def save(self, commit = True):
        return super(LibrarianAdminForm, self).save(commit = commit)


class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'library', 'contact_number')
    ordering = ('first_name',)
    list_filter = ('library__name',)
    search_fields = ['first_name','middle_name', 'last_name',]
    form = LibrarianAdminForm

admin.site.register(Librarian, LibrarianAdmin)


class BookAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        isbn = self.cleaned_data.get('isbn')
        total_stock = self.cleaned_data.get('total_stock')
        available_stock = self.cleaned_data.get('available_stock')
        if isbn is not None:
            regex = r"^(\d{3})(\s|\-)(\d{1,5})(\s|\-)(\d{1,7})(\s|\-)(\d{1,6})(\s|\-)(\d)$"
            match = re.search(regex, isbn)
            if match is None:
                raise forms.ValidationError("ISBN should be in the format xxx-x{repeated once to 5 times}-x{repeated once to 7 times}-x{repeated once to 6 times}-x",
                                            code = 'invalid')
        if available_stock != total_stock:
            raise forms.ValidationError("Stock mismatch. Available stock must be equal to Total stock")

        return self.cleaned_data

    def save(self, commit = True):
        return super(BookAdminForm, self).save(commit = commit)

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'author_name', 'publication', 'isbn', 'library', 'total_stock', 'available_stock', 'available', 'price',)
    list_filter = ('available', 'library',)
    ordering = ('book_name',)
    search_fields = ['book_name', 'author_name', 'publication',]
    form = BookAdminForm

admin.site.register(Book, BookAdmin)

class MemberAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemberAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number is not None:
            regex = r"^(\d{10})$"
            match = re.search(regex, contact_number)
            if match is None:
                raise forms.ValidationError("Contact number should be 10 digits", code = 'invalid')
        return self.cleaned_data

    def save(self, commit = True):
        return super(MemberAdminForm, self).save(commit = commit)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'membership', 'address', 'contact_number',)
    list_filter = ('membership',)
    ordering = ('first_name',)
    search_fields = ['first_name','middle_name', 'last_name',]
    form = MemberAdminForm

admin.site.register(Member, MemberAdmin)

class IssueRecordAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IssueRecordAdminForm, self).__init__(*args, **kwargs)
        if not self.instance.id:
            self.fields['returned'].disabled = True
            self.fields['date_returned'].disabled = True
        else:
            self.fields['book_borrowed'].disabled = True
            self.fields['issued_librarian'].disabled = True
            self.fields['date_of_issue'].disabled = True
            self.fields['date_of_return'].disabled = True
            self.fields['member'].disabled = True
            self.fields['penalty_per_day'].disabled = True

    def clean(self):
        book = self.cleaned_data.get('book_borrowed')
        book_count = self.cleaned_data.get('book_count')
        if book_count == 0:
            raise forms.ValidationError("The member has reached the limit of 4 books per person. Please return a book to borrow another one.")
        if self.cleaned_data.get('returned') == False:
            if self.cleaned_data.get('date_returned') is None:
                if book.available == False:
                    raise forms.ValidationError("Entered book not in stock. Please enter a different book.", code = 'invalid')
            else:
                raise forms.ValidationError("Please check Returned field and continue.")
        else:
            if self.cleaned_data.get('date_returned') is None:
                raise forms.ValidationError("Please the enter the Date returned field and continue.")
        return self.cleaned_data

    def save(self, commit = True):
        return super(IssueRecordAdminForm, self).save(commit = commit)


class IssueRecordAdmin(admin.ModelAdmin):
    list_display = ('book_borrowed', 'member', 'date_of_issue', 'date_of_return', 'penalty_per_day', 'issued_librarian', 'date_returned', 'returned', 'fine_imposed',)
    list_filter = ('issued_librarian__library', 'returned',)
    search_fields = ['book_borrowed', 'issued_librarian', 'member',]
    form = IssueRecordAdminForm

admin.site.register(IssueRecord, IssueRecordAdmin)

