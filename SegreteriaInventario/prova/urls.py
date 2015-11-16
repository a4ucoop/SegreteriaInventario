from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^local/', views.showLocalDB, name='showLocalDB'),
    url(r'^remote/', views.showRemoteDB, name='showRemoteDB'),
    url(r'^update/partial', views.checkUpdate, name='checkUpdate'),
    url(r'^update/complete', views.updateLocalDB, name='updateLocalDB'),
]
