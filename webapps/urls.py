from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'SimSimWeb.views.home'),
    url(r'register', 'SimSimWeb.views.register', name='register'),
    url(r'login', 'django.contrib.auth.views.login', {'template_name': 'SimSimWeb/login.html'}),
    url(r'introduction', 'SimSimWeb.views.introduction'),
    url(r'guest_request', 'SimSimWeb.views.dashboard', name='guest_request'),
    url(r'dashboard/guest_list', 'SimSimWeb.views.guest_list'),
    url(r'dashboard/family', 'SimSimWeb.views.family'),
    url(r'dashboard/lock_activity', 'SimSimWeb.views.lock_activity'),
    url(r'dashboard/manage_properties', 'SimSimWeb.views.manage_properties'),
    url(r'dashboard/profile', 'SimSimWeb.views.profile'),
)
