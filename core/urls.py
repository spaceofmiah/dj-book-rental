from django.urls import path, include
from django.contrib import admin
from django.views import generic
from .views import auth

urlpatterns = [
    path('', generic.TemplateView.as_view(template_name='index.html'), name='index'),
    path('rentals/', include('rentals.urls', namespace='rentals')),
    path('register', auth.signup, name='register'),
    path('logout', auth.signout, name='logout'),
    path('login', auth.signin, name='login'),
    path('admin/', admin.site.urls),
]
