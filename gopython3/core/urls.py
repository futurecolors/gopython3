# coding: utf-8
from django.conf.urls import patterns, url, include
from core.rest import router, PackageView, PackageListView


urlpatterns = patterns('',
    url(r'', include(router.urls)),
    url(r'^packages/$', PackageListView.as_view(), name='spec-list'),
    url(r'^packages/(?P<code>.+)/$', PackageView.as_view(), name='spec-detail'),
)
