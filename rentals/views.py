from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
import requests


@login_required(redirect_field_name='redirect', login_url='/login')
def dashboard(request:HttpRequest):
    return render(request, 'dashboard.html')


@login_required(redirect_field_name='redirect', login_url='/login')
def rent(request:HttpRequest):
    """
    Processes book rentage request. This allows a student to rent
    a book for a specified number of days. 

    Returns a HttpResponseRedirect 

    Query Params:
    
    : book_name [str]: Actual book name to be rented (this should be the title from open library)

    : student [str]: Student's email address - this should be a valid email address in the database

    : return date [date str]: A valid date string signifying the date the rentage is to last for.
    """
    book_name = request.POST.get('book_name')
    student = request.POST.get('student')
    return_date = request.POST.get('return_date')
    print(book_name, student, return_date)
    return HttpResponseRedirect(reverse('index'))



def htmx_book_search(request:HttpRequest):
    """
    Processes request that searches for book using it's title from 
    openlibrary.

    The processed request returns an HTMLResponse containing the
    search result

    Query Params:

    : book [str]: The book title which is to be searched for
    """
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


def htmx_rentage_price(request:HttpRequest):
    """
    Processes request that calculates the price of a rentage.

    The processed request returns an HTMLResponse containing the
    calculated price

    Query Params:

    : return_date [date str]: A valid date string signifying the date the rentage is to last for.

    : num_pages [int]: The number of pages in the book to be rented
    """
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

