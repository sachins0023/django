# Generated by Django 2.2.6 on 2019-10-14 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0008_book_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.CharField(max_length=20)),
                ('return_date', models.CharField(max_length=20)),
                ('borrower_name', models.CharField(max_length=50)),
                ('book_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.Book')),
            ],
        ),
    ]
