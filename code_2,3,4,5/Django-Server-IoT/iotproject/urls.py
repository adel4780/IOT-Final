from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.firstPage, name='first_page'),
    path('on', views.get_on, name='get_on'),
    path('off', views.get_off, name='get_off'),
    path('schedule', views.schedule, name='schedule'),
    path('getStatus', views.getStatus, name='getStatus'),
]
