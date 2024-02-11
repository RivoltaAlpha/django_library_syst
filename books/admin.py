from django.contrib import admin
from .models import Book, Student, IssuedBook

   # Define a custom method to compute the status
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'genre', 'get_status', 'user')
    list_filter = ('genre',)
    search_fields = ('title', 'author', 'isbn', 'user__username')

    def get_status(self, obj):
        return obj.status

    get_status.short_description = 'Status'


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'course', 'phone', 'fine_amount')
    search_fields = ('user__username', 'first_name', 'last_name')



class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'issued_date', 'expiry_date', 'return_date')
    list_filter = ('issued_date', 'expiry_date', 'return_date')
    search_fields = ('student__user_username', 'book_title')

admin.site.register(Book, BookAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(IssuedBook, IssuedBookAdmin)
