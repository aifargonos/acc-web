from django.conf.urls import url

from . import views

app_name = 'accountancy'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^import/$', views.import_view, name='import_view'),
]