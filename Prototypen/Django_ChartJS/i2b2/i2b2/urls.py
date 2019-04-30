"""
i2b2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

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

# Uncomment next two lines to enable admin:
#from django.contrib import admin
#from django.urls import path
from django.conf.urls import url
from django.contrib import admin
import mep.views

urlpatterns = [
    # Uncomment the next line to enable the admin:
    #path('admin/', admin.site.urls)
   
    url(r'^$', mep.views.index, name ='index'),
    url(r'^sex$', mep.views.sex, name ='sex'),
    url(r'^race$', mep.views.race, name ='race'),
    url(r'^nationality$', mep.views.nationality, name ='nationality'),
    url(r'^relationship$', mep.views.relationship, name ='relationship'),
    url(r'^religion$', mep.views.religion, name ='religion'),
    url(r'^income$', mep.views.income, name ='income')

]
