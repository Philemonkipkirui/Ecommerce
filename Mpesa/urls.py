from django.urls import path
from . import views

urlpatterns = [
    path('validation/', views.c2b_validation, name='c2b_validation'),
    path('confirmation/', views.c2b_confirmation, name='c2b_confirmation'),
    path('simulate-payment/', views.simulate_payment, name='simulate-payment'),
    path('stk/<int:product_id>/', views.lipa_na_mpesa_online, name = 'lipa_na_mpesa_online'),
    path('stk-callback/', views.stk_callback, name='stk_callback'),
]
