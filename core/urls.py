from django.urls import path, include
from django.views import generic
from .views import auth

# setup url configuration to serve media asset
from django.conf import settings

urlpatterns = [
    path('', generic.TemplateView.as_view(template_name='index.html'), name='index'),
    path('rentals/', include('rentals.urls', namespace='rentals')),
    path('register', auth.signup, name='register'),
    path('logout', auth.signout, name='logout'),
    path('login', auth.signin, name='login'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)