from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="base/index.html"), name='index'),
    url(r'^acc/', include('docker_django.apps.accountancy.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
