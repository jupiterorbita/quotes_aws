from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^quotes_html$', views.quotes_html),
    url(r'^quotes_add_method$', views.quotes_add_method),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^edit_method$', views.edit_method),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^likes/(?P<id>\d+)$', views.likes),
    url(r'^logout$', views.logout)
]