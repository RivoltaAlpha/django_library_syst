from django.urls import path
from . import views

urlpatterns = [
    #USER
    path("welcome/", views.home, name="home"),
    path('login/', views.student_login_view, name='login'),
    path("logout/", views.logout, name="logout"),

    path("Student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("my_books/<int:myid>/", views.user_books, name="user_books"),
    path('booking/', views.booking_list, name='booking_list'),
    path('book/<int:book_id>/', views.book_booking, name='book_booking'),
    path("profile/", views.profile, name="profile"),
    # path("edit_profile/", views.edit_profile, name="edit_profile"),
    # path("change_password/", views.change_password, name="change_password"),


    #   ADMIN
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("add_book/", views.add_book, name="add_book"),
    path("view_books/", views.view_books, name="view_books"),
    path("view_students/", views.view_students, name="view_students"),
    path("issue_book/", views.issue_book, name="issue_book"),
    # path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    # path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
]