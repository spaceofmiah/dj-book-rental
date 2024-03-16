from django.contrib import admin
from django.views import generic
from django.urls import path, include

urlpatterns = [
    path('', generic.TemplateView.as_view(template_name='index.html'), name='index'),
    path('rentals/', include('rentals.urls', namespace='rentals')),
    path('admin/', admin.site.urls),
]
