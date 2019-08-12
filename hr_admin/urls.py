from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("",views.index,name="index"),
    path("accounts/registration",views.signup,name="signup"),
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),
    path('activate/password/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate_user, name='activate_user'),
    path("accounts/login/",views.user_login,name="login"),
    path("accounts/logout/",views.user_logout,name="logout"),
    path("accounts/dashboard/",views.dashboard,name='dashboard'),
    path("accounts/password/",views.new_password,name='password'),
    path("assest/asign/",views.asset_ajax,name='asset'),
    path("assest/admin/view/",views.view_assests,name='assest_view'),
    path("user/profile/",views.employee_profile,name='profile'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
