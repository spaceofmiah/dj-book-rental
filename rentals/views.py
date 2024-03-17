from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .utils import compute_price
from django.urls import reverse
from . import models, forms
import requests



@login_required(redirect_field_name='redirect', login_url='/login')
def rentals(request:HttpRequest):
    return render(
        request, 
        'rentals.html', 
        context={
            'rentals': models.Rental.objects.all(), 
            'active': 'rentals'
        }
    )


@login_required(redirect_field_name='redirect', login_url='/login')
def students(request:HttpRequest):
    if request.method == "GET":
        return render(
            request, 
            'students.html', 
            context={
                'students': models.Student.objects.all().order_by('-created_at'), 
                'active': 'students'
            }
        )
    
    form = forms.NewStudentForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        return render(
            request,
            'students.html',
            context={
                'students': models.Student.objects.all().order_by('-created_at'),
                'active': 'students',
                'form': form
            }
        )
    
    try:
        models.Student.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email']
        )
    except IntegrityError:
        messages.add_message(request, messages.ERROR, 'Student with the given email already exists')
        return HttpResponseRedirect(reverse('rentals:students'))

    messages.add_message(request, messages.SUCCESS, "New student added successfully")
    return HttpResponseRedirect(reverse('rentals:students'))


@login_required(redirect_field_name='redirect', login_url='/login')
def books(request:HttpRequest):
    return render(
        request, 'books.html', 
        context={
            'books': models.Book.objects.all(), 
            'active': 'books'
        }
    )
    


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
    form = forms.NewRentalForm(request.POST)

    if not form.is_valid():
        return render(request, 'rentage_cost.html', {'form': form})
    
    student = form.cleaned_data['student']
    book_name = form.cleaned_data['book_name']
    return_date = form.cleaned_data['return_date']

    try:
        student = models.Student.objects.get(email=student)
    except models.Student.DoesNotExist:
        messages.add_message(request, messages.ERROR, f'No student found for the given email : {student}')
        return HttpResponseRedirect(reverse('rentals:index'))
    
    is_book_from_db = False
    # attempt to retrieve book from the database with the given name. 
    # If the book is not found, attempt to retrieve from openlibrary.
    try:
        book:models.Book = models.Book.objects.get(title=book_name)
        title = book.title
        author_name = book.author
        pages = book.total_pages
        is_book_from_db = True
    except models.Book.DoesNotExist:
        try:
            response = requests.get(f"https://openlibrary.org/search.json?title={book_name}")
            data = response.json()['docs'][0]
            title = data['title']
            author_name = data['author_name'][0]
            pages = data['number_of_pages_median']
        except Exception as e:
            messages.add_message(
                request, 
                messages.ERROR, 
                f'Unable to retrieve book with the given title: {book_name}'
            )
            return HttpResponseRedirect(reverse('rentals:index'))

    try:
        price = compute_price(return_date, pages)
    except ValueError:
        return render(request, 'rentage_cost.html', {'error': 'Return date cannot be a past date'})


    # create a transaction to create a book and create rentage for the book
    try:
        with transaction.atomic():
            if not is_book_from_db:
                book = models.Book.objects.create(
                    title=title,
                    total_pages=pages,
                    author=author_name,
                )

            models.Rental.objects.create(
                book=book, 
                cost=price,
                student=student, 
                end_date=return_date, 
            )
    except Exception as e:
        messages.add_message(
            request,
            messages.ERROR,
            f'Unable to create book with the given title: {book_name}'
        )
        return HttpResponseRedirect(reverse('rentals:index'))

    return HttpResponseRedirect(reverse('rentals:index'))


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


def htmx_find_student(request:HttpRequest):
    page = request.GET.get('page', 'rentals')
    
    if page == 'students':
        student = models.Student.objects.filter(email__iexact=request.GET.get('email')).first()
        return render(request, 'find_student.html', context={
            "student_name": "email taken" if student else ""
        })

    student = models.Student.objects.filter(email__startswith=request.GET.get('student')).first()
    return render(request, 'find_student.html', context={
        "student_name": student.name if student else "no match found"
    })


def htmx_rentage_price(request:HttpRequest):
    """
    Processes request that calculates the price of a rentage.

    The processed request returns an HTMLResponse containing the
    calculated price

    Query Params:

    : return_date [date str]: A valid date string signifying the date the rentage is to last for.

    : num_pages [int]: The number of pages in the book to be rented
    """
    return_date = request.GET.get('return_date')
    num_pages = request.GET.get('book_pages')
    if not return_date or not num_pages:
        return render(request, 'rentage_cost.html', {'error': "Pricing failed. Ensure all fields are filled"})
    
    
    return_date_value = timezone.datetime.strptime(request.GET.get('return_date'), '%Y-%m-%d').date() 

    try:
        price = compute_price(return_date_value, num_pages)
    except ValueError:
        return render(request, 'rentage_cost.html', {'error': 'Return date cannot be a past date'})
    
    return render(request, 'rentage_cost.html', {'return_date': return_date, 'num_pages': num_pages, 'error': None, 'price': price})

