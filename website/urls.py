
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vote/', views.vote, name='vote'),
    path('facials/', views.facial_auth, name='facials'),
    path('verify/', views.otp_verify, name='verify'),
]
