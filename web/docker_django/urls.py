from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^acc/', include('docker_django.apps.accountancy.urls', namespace="accountancy")),
    url(r'^admin/', include(admin.site.urls)),
]
