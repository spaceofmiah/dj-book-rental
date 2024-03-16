from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib import admin
from django.views import generic
from django.urls import path, reverse
from django.contrib import messages
import requests 


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


urlpatterns = [
    path('dashboard/', generic.TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('', generic.TemplateView.as_view(template_name='index.html'), name='index'),
    path('search/', search, name='search'),
    path('rent/', rent, name='rent'),
    path('admin/', admin.site.urls),
]
