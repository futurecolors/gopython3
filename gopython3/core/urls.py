# coding: utf-8
from django.conf.urls import patterns, url, include
from core.rest import router, PackageView


urlpatterns = patterns('',
    url(r'', include(router.urls)),
    url(r'^packages/(?P<code>.+)/$', PackageView.as_view(), name='spec-detail'),
)
