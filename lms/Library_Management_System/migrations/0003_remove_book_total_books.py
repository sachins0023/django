# Generated by Django 2.2.6 on 2019-10-17 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Library_Management_System', '0002_auto_20191017_0426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='total_books',
        ),
    ]
