from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^local/', views.showLocalDB, name='showLocalDB'),
    url(r'^remote/', views.showRemoteDB, name='showRemoteDB'),
    url(r'^update/partial', views.checkUpdate, name='checkUpdate'),
    url(r'^update/complete', views.updateLocalDB, name='updateLocalDB'),
    url(r'^show/([0-9]+)/$', views.showSingleItem, name='showSingleItem'),
    url(r'^examples/bootstrap_table/data', views.getData, name='getData'),
    url(r'^accounts/login/$', views.login, {'template_name': 'registration/login.html'}, name = 'login'),
    url(r'^accounts/registration/$', views.registration),
	url(r'^upload/$', views.uploadPicture),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
