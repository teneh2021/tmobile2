"""tmobile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from os import name
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.urls.conf import include
from tmo_amara import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # App specific settings
    
    path('index', views.user_home, name='user_home'),
    path('ss', views.welcome, name='welcome'),
    path('make_payment', views.make_payment, name='make_payment'),
    path('payment_history', views.payment_history, name='payment_history'),
    path('upload', views.Uploadw.as_view(), name= 'upload'),
    path('message', views.Messagew.as_view(), name='message'),
    path('ussd_code', views.ussd_code, name= 'ussd_code'),
    path('', views.user_login, name='login'),
     path('logout/', views.user_logout, name='logout'),
    path('index', views.user_home, name='index'),
    path('tmo_amara', include('tmo_amara.urls')),
    path('tmo_amara', include('django.contrib.auth.urls') ),
    path("favicon.ico", RedirectView.as_view(
        url=staticfiles_storage.url("favicon.ico")), ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    

else:
    urlpatterns += staticfiles_urlpatterns()
    
"""
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


      
                                
"""  
