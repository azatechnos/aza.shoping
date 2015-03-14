from django.conf.urls import patterns, include, url
from django.contrib import admin
from dashboard.views import DashBoardView

urlpatterns = patterns('',
                       url(r'^$', DashBoardView.as_view(), name='home'),
)
