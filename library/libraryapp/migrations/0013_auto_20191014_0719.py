# Generated by Django 2.2.6 on 2019-10-14 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0012_auto_20191014_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]