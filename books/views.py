from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book,Student,IssuedBook
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.views.generic import DetailView
import logging


#ADMIN
# Dashboard
def admin_dashboard(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for issued_book in issuedBooks:
        days = (date.today() - issued_book.issued_date).days
        fine = max(0, days - 14) * 5
        student.fine_amount += fine  # Update the student's fine amount
        student.save()
        book = Book.objects.get(isbn=issued_book.isbn)
        student = Student.objects.get(pk=issued_book.student_id)
        detail = (student.user.username, student.user_id, book.title, book.isbn, issued_book.issued_date, issued_book.expiry_date, fine)
        details.append(detail)

    return render(request, "dashboard.html", {'issuedBooks': issuedBooks, 'details': details})

def add_book(request):
    if request.method =='POST':
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']
        image = request.POST['image']

        book = Book.objects.create(title=title, author=author,isbn=isbn, genre=genre, image=image )
        book.save()
        alert = True
        return render(request, "add_book.html", {'alert':alert})

        return redirect('view_books')

    return render(request, 'add_book.html')

#issue book
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.student_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()
            alert = True
            return render(request, "issue_book.html", {'obj':obj, 'alert':alert})

    return render(request, "issue_book.html", {'form':form})

#view all books
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books':books})


#view all students
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students})

# view profile
@login_required
def profile(request):
    return render(request, "profile.html")



#STUDENT 

@login_required
def update_profile(request):
    context = context_data(request)
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)

@login_required
def update_password(request):
    context =context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)
    
# Home page 
def home(request):
    return render(request, 'home.html')

#Logout Function
def logout_user(request):
    logout(request)
    return redirect('home')

logger = logging.getLogger(__name__)

# Student Login
def student_login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            logger.info(f"User {user} logged in successfully")
            return redirect('student_dashboard')  # Change to your URL
        else:
            logger.warning("Authentication failed")
            error_message = 'Invalid email or password. Please try again.'
  

    else:
        error_message = None

    return render(request, 'student/login.html', {'error_message': error_message})

# returns booking view
def booking_list(request):
    available_books = Book.objects.filter(issuedbook__isnull=True)
    return render(request, 'student/booking_list.html', {'available_books': available_books})


# Booking process
def book_booking(request, book_id):
    book = Book.objects.get(id=book_id)
    student = request.user.student

    if IssuedBook.objects.filter(book=book, return_date__isnull=True).exists():
        return render(request, 'book_booking_failed.html', {'book': book})

    IssuedBook.objects.create(student=student, book=book, issued_date=date.today(), expiry_date=expiry())
    return render(request, 'book_booking_success.html', {'book': book})

# Recommended books in dashboard
def student_dashboard(request):
    user = request.user
    student = request.user.student.course
    available_books = Book.objects.filter(status='available')

    # Handling search functionality
    genre_query = request.GET.get('genre', '')
    title_query = request.GET.get('title', '')

    if genre_query:
        available_books = available_books.filter(genre__icontains=genre_query)

    if title_query:
        available_books = available_books.filter(title__icontains=title_query)

    context = {
        'user': user,
        'student': student,
        'available_books': available_books,
        'genre_query': genre_query,
        'title_query': title_query,
    }

    return render(request, 'student/dashboard.html', context)

# Students Books
def user_books(request):
    user = request.user
    user_books = Book.objects.filter(user=request.user)  
    context = {'user_books': user_books}
    return render(request, 'books.html', context)

# Student Profile
@login_required
def profile(request):
    return render(request, "student/profile.html")
