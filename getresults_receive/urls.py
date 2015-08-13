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

from .views import DashboardView, user_login, ReceiveView, ReceiveSampleView, ReceiveBatchView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', user_login, name='login_url'),
    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
    url(r'^receive/', ReceiveView.as_view(), name='receive'),
#     url(r'^receive_batch/', ReceiveBatchView.as_view(), name='receive_batch'),
#     url(r'^receive_sample/', ReceiveSampleView.as_view(), name='receive_sample'),
)
