from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.otp_login, name= "otp_login"),
    path("verify/", views.verify_otp, name= "verify_otp"),
    path("logout/", views.user_logout, name= "logout"),
    path("register/", views.register, name= "register"),
]