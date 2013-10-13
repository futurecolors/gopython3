from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView


class FrontendRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return '/#' + self.request.path


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='frontend/index.html'), name='index'),
    url(r'$', FrontendRedirectView.as_view()),
)
