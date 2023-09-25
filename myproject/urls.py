"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from myapp.views import (
    register_view, login_view, logout_view, dashboard, Employee_view, index, about,
    anouncement, contacts, Employer_dashboard, Inventory, profile,
    )

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/register/', register_view, name='register'),
    path('Employee/', Employee_view, name='Employee'),
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('anouncement/', anouncement, name='anouncement'),
    path('contacts/', contacts, name='contacts'),
    path('Employer_dashboard/', Employer_dashboard, name='Employer_dashboard'),
    path('Inventory/', Inventory, name='Inventory'),
    path('profile/', profile, name='profile'),
    # path('images/', include('myapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)