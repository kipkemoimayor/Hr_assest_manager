from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("accounts/registration",views.signup,name="signup"),
    path('^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),
]
