# Generated by Django 2.2.6 on 2019-10-14 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0010_auto_20191014_0451'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]
