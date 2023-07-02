from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('detail_news/', views.detail_news, name='detail_news'),
    path('detail_books/', views.detail_books, name='detail_books'),
]