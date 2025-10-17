"""
URL configuration for epmiti project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.index, name='index'),
    path('about/', core_views.about, name='about'),
    path('contact/', core_views.contact, name='contact'),
    path('blog/', core_views.blog, name='blog'),
    path('gallery/', core_views.gallery, name='gallery'),
    path('events/', core_views.events, name='events'),
    path('donation/', core_views.donation, name='donation'),
    path('volunteer/', core_views.volunteer, name='volunteer'),
    path('service/', core_views.service, name='service'),
    path('causes/', core_views.causes, name='causes'),
]
