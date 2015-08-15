"""xx URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url, patterns
from django.contrib import admin

from getresults_receive.admin import admin_site
from .views import DashboardView, login_view, logout_view, ReceiveView, show_batch


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin_site.urls)),
    url(r'^accounts/login/', login_view, name='login_url'),
    url(r'^login/', login_view, name='login_url'),
    url(r'^logout/', logout_view, name='logout_url'),
    url(r'^home/', ReceiveView.as_view(), name='home'),
    url(r'^receive/', ReceiveView.as_view(), name='receive'),
    url(r'^batch/(?P<batch_identifier>[0-9A-Z\-]+)/', show_batch, name='batch'),
    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
    url(r'^$', login_view, name='login_url'),
)
