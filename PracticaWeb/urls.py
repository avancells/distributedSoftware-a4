"""PracticaWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from rest_framework import routers
from ykea import views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    url(r'^ykea$', RedirectView.as_view(url='ykea/home', permanent=False), name='index'),
    url(r'^ykea/$', RedirectView.as_view(url='home', permanent=False), name='index'),
    url(r'^ykea/', include('ykea.urls'), name='ykea'),
    url(r'^admin/', admin.site.urls),
    url(r'^ykea/accounts/login/$',  login, name='login'),
    url(r'^ykea/accounts/logout/$', logout, name='logout'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', RedirectView.as_view(url='ykea/home', permanent=False), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
