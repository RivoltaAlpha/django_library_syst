# Generated by Django 4.2.2 on 2023-09-13 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(default='example@kyu.com', max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='student',
            name='reg_no',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
