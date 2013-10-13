from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('')

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^(favicon.ico)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

urlpatterns += patterns('',
    url(r'^api/v1/', include('core.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('frontend.urls')),
)
