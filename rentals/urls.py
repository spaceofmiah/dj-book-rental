from django.urls import path
from . import views

app_name = 'rentals'
urlpatterns = [
    path('rentage-price/', views.htmx_rentage_price, name='validate'),
    path('book-search/', views.htmx_book_search, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rent/', views.rent, name='rent'),
]