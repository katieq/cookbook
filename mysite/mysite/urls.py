"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from mysite.views import hello, current_datetime, hours_ahead

urlpatterns = [
               url(r'^admin/', include(admin.site.urls)),
               #url(r'^mentions/', include('mentions.urls')),
               url(r'^hello/$', hello),
               #url(r'^time/$', current_datetime),
               #url(r'^time/plus/(\d{1,2})/$', hours_ahead),
               url(r'^cooklog/', include('cooklog.urls')),
               
               ] + static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT) # not sure if need this.. a random site suggested while attempting image upload, jan-11-2017
