from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_control.urls')),
    path('app/', include('app_control.urls')),
]