from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^local/', views.showLocalDB, name='showLocalDB'),
    url(r'^remote/', views.showRemoteDB, name='showRemoteDB'),
    url(r'^update/partial', views.checkUpdate, name='checkUpdate'),
    url(r'^update/complete', views.updateLocalDB, name='updateLocalDB'),
    url(r'^show/([0-9]+)/$', views.showSingleItem, name='showSingleItem'),
    url(r'^examples/bootstrap_table/data', views.getData, name='getData'),
    url(r'^accounts/login/$', views.login, {'template_name': 'registration/login.html'}),
    url(r'^accounts/registration/$', views.registration),
]
