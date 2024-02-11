from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.urls import path, include

 
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    genre = models.CharField(max_length=50)
    image = models.ImageField(upload_to=" ", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    STATUS_CHOICES = [
        ("Due", "Due"),
        ("checked_out", "Checked Out"),
        ("Available", "Available"),
        ('reserved', 'Reserved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    @property
    def calculate_status(self):
        today = date.today()
        if IssuedBook.objects.filter(book=self, return_date__isnull=True).exists():
            issued_book = IssuedBook.objects.get(book=self, return_date__isnull=True)
            if today > issued_book.expiry_date:
                return "Due"
            else:
                return "Issued"
        else:
            return "Available"
 
    def __str__(self):
        return str(self.title) + "[" + str(self.isbn) + "]"

    class Meta:
        ordering = ['title']


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email= models.CharField(max_length=30, blank=False, default='example@kyu.com')
    course = models.CharField(max_length=50, blank=False)
    reg_no = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
 
    def __str__(self):
        return f"{self.user.username} [{self.reg_no}]"

    class Meta:
        ordering = ['reg_no']

def expiry():
    return datetime.today() + timedelta(days=14)
    
class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.book.title}"