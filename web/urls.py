from django.urls import path
from . import views
from django.views.static import serve


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
]
