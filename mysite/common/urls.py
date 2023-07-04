from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    # path('login/', views.LogIn, name='login'),
    path('login/', views.LogIn, name='login'),
    path('logout/', views.LogOut, name='logout'),
    path('signup/', views.SignUp, name='signup'),
    path('subscribe/', views.Subscribe, name='subscribe'),
]