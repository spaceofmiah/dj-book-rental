
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from ..forms import auth


def signin(request:HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=reverse('index'))
    
    if request.method == "GET":
        return render(request, 'auth/signin.html')
    
    form = auth.SignInForm(request.POST)
    if not form.is_valid():
        return render(
            request, 'auth/signin.html', {'error': 'Invalid authentication credentials'}
        )

    user = authenticate(
        username=form.cleaned_data['email'], 
        password=form.cleaned_data['password']
    )
        
    if not user:
        return render(
            request, 'auth/signin.html', {'error': 'Invalid authentication credentials'}
        )

    login(request, user=user)
    redirect_to = request.GET.get('redirect', reverse('rentals:index'))
    return HttpResponseRedirect(redirect_to=redirect_to)


def signout(request:HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    
    return HttpResponseRedirect(redirect_to=reverse('index'))


def signup(request:HttpRequest):
    if request.method == "GET":
        return render(request, 'auth/signup.html')
    
    signup_form = auth.SignUpForm(request.POST)
    if not signup_form.is_valid():
        return render(request, 'auth/signup.html', {'form': signup_form})
    
    user_exists = get_user_model().objects.filter(email=signup_form.cleaned_data['email']).exists()
    if user_exists:
        return render(request, 'auth/signup.html', {'error': 'User already exists', 'form': signup_form})
    
    try:
        user = get_user_model().objects.create_user(
            email=signup_form.cleaned_data['email'],
            name=signup_form.cleaned_data['name']
        )
        user.is_active = True
        user.set_password(signup_form.cleaned_data['password'])
        user.save()
    except Exception as e:
        return render(request, 'auth/signup.html', {'error': str(e)})
    
    login(request, user=user)
    redirect_to = request.GET.get('redirect', reverse('rentals:index'))
    return HttpResponseRedirect(redirect_to=redirect_to)
