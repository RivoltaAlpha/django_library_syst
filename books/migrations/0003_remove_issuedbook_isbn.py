# Generated by Django 4.2.2 on 2023-09-09 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuedbook',
            name='isbn',
        ),
    ]