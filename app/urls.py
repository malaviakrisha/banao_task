from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path("main",views.main,name="main"),
    path("signin_1/", views.signin_1, name="signin_1"),
    path("signup_1/", views.signup_1, name="signup_1"),
    path("signin_2/", views.signin_2, name="signin_2"),
    path("signup_2/", views.signup_2, name="signup_2"),
    path("patient_d/",views.patient_d,name="patient_d"),
    path("doctor_d/",views.doctor_d,name="doctor_d"),
    path("userlogout/", views.userlogout, name="userlogout"),]