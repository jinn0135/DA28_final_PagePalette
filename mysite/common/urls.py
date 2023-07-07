from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', views.LogIn, name='login'),
    path('logout/', views.LogOut, name='logout'),
    path('signup/', views.SignUp, name='signup'),
    path('subscribe/', views.Subscribe, name='subscribe'),
    path('subscribe_book/', views.subscribe_book, name='subscribe_book'),
    path('subscribe_book/book2/', views.subscribe_book2, name='subscribe_book2'),
    path('subscribe_book/book2/success/', views.subscribe_success, name='subscribe_success'),
]