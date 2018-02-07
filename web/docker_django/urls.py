from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="base/index.html"), name='index'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^acc/', include('docker_django.apps.accountancy.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
