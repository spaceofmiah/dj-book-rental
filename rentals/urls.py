from django.urls import path
from . import views

app_name = 'rentals'
urlpatterns = [
    path('find-student/', views.htmx_find_student, name='find_student'),
    path('rentage-price/', views.htmx_rentage_price, name='validate'),
    path('book-search/', views.htmx_book_search, name='search'),
    path('extend-rent/<int:id>/', views.extend_rent, name='extend_rent'),
    path('students/', views.students, name='students'),
    path('books/', views.books, name='books'),
    path('rent/', views.rent, name='rent'),
    path('', views.rentals, name='index'),
]