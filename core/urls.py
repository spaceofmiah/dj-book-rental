from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from django.contrib import admin
from django.views import generic
import requests 

# TODO: UI
# - set the number of pages as an hidden value to an input field
# - when return date is selected, retrieve the number of pages and compute
#   either the user is eligible for free tier or would pay subscription fee (client side)
# - display the amount payable by the student


# TODO: Backend
# - setup account/user model
# - setup book model
# - setup rent model

def search(request:HttpRequest):
    try:
        response = requests.get(f"https://openlibrary.org/search.json?title={request.GET.get('book')}")
        data = response.json()['docs'][0]
        title = data['title']
        author_name = data['author_name'][0]
        pages = data['number_of_pages_median']
    except:
        author_name = None
        pages = None
        title = None

    return render(request, 'search.html', {'author_name': author_name, 'pages': pages, 'title':title})

def rent(request:HttpRequest):
    book_name = request.POST.get('book_name')
    student_name = request.POST.get('student')
    return_date = request.POST.get('return_date')
    print(book_name, student_name, return_date)
    return HttpResponseRedirect(reverse('index'))

def validate(request:HttpRequest):
    current_date = timezone.now().date()
    return_date = request.GET.get('return_date')
    num_pages = request.GET.get('book_pages')
    if not return_date or not num_pages:
        return render(request, 'rentage_cost.html', {'error': "Pricing failed. Ensure all fields are filled"})
    
    
    return_date_value = timezone.datetime.strptime(request.GET.get('return_date'), '%Y-%m-%d').date() 
    if return_date_value < current_date:
        return render(request, 'rentage_cost.html', {'error': 'Return date cannot be a past date'})
    
    if return_date_value.month == current_date.month:
        price = 0
    else:
        price = int(num_pages) / 100
    
    return render(request, 'rentage_cost.html', {'return_date': return_date, 'num_pages': num_pages, 'error': None, 'price': price})



urlpatterns = [
    path('dashboard/', generic.TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('', generic.TemplateView.as_view(template_name='index.html'), name='index'),
    path('validate/', validate, name='validate'),
    path('search/', search, name='search'),
    path('rent/', rent, name='rent'),
    path('admin/', admin.site.urls),
]
