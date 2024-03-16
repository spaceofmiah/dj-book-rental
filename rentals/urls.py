from django.views import generic
from django.urls import path
from . import views

app_name = 'rentals'
urlpatterns = [
    path('dashboard/', generic.TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('rentage-price/', views.htmx_rentage_price, name='validate'),
    path('book-search/', views.htmx_book_search, name='search'),
    path('rent/', views.rent, name='rent'),
]