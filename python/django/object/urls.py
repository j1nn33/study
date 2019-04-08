"""conceptdebbase URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('object/', include('object.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    #path('', RedirectView.as_view(url='/object/', permanent=True)), # редирек  с '' на /object/
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
    #path('', RedirectView.as_view(url='/accounts/', permanent=True)), # редирек  с '' на /object/
    #path('', RedirectView.as_view(url='/accounts/login.html', permanent=True)), # редирек  с '' на /object/
  ]


#Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),

]
