from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("accounts/registration",views.signup,name="signup"),
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),
    path("accounts/login/",views.user_login,name="login"),
    path("accounts/logout/",views.user_logout,name="logout"),
    path("accounts/dashboard/",views.dashboard,name='dashboard'),

]
