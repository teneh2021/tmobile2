from os import name
from tmo_amara import views
from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage



app_name = 'tmo_amara'

urlpatterns = [

    # App specific settings
   
    path('index', views.user_home, name='user_home'),
    path('welcome', views.welcome, name='welcome'),
    path('make_payment', views.make_payment, name='make_payment'),
    path('payment_history', views.payment_history, name='payment_history'),
    path('upload', views.Uploadw.as_view(), name='upload'),
    path('message', views.Messagew.as_view(), name = 'message'),
    path('ussd_code', views.ussd_code, name='ussd_code'),
    path('', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('index', views.user_home, name='index'),
    path("favicon.ico", RedirectView.as_view(
        url=staticfiles_storage.url("favicon.ico")), ),

]

