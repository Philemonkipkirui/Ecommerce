from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    #path('', views.home, name= 'home'),
    path('register/', views.register, name='register'), 
    path('login/', LoginView.as_view (template_name = 'Accounts/login.html'), name='login'),
    #path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout'),
]
