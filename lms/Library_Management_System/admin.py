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
    search_fields = ['library','fullname']
    form = LibrarianAdminForm

admin.site.register(Librarian, LibrarianAdmin)