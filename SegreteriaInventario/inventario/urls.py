from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^local/', views.showLocalDB, name='showLocalDB'),
    url(r'^inventario$', views.showLocalDB, name='showLocalDB'),
    # url(r'^remote/', views.showRemoteDB, name='showRemoteDB'),
    url(r'^update/partial', views.checkUpdate, name='checkUpdate'),
    url(r'^update/complete', views.updateLocalDB, name='updateLocalDB'),
    url(r'^show/([0-9]+)/$', views.showSingleItem, name='showSingleItem'),
    url(r'^table/getData', views.getData, name='getData'),
    url(r'^table/advancedSearch$', views.advancedSearch, name='advancedSearch'),
    url(r'^table/editable/editAccurateLocation', views.editAccurateLocation, name='editAccurateLocation'),
    url(r'^table/editable/getAccurateLocationList', views.getAccurateLocationList, name='getAccurateLocationList'),
    url(r'^table/editable/addAccurateLocation', views.addAccurateLocation, name='addAccurateLocation'),  
    url(r'^accounts/login/$', views.login, {'template_name': 'registration/login.html'}, name = 'login'),
	url(r'^upload/immagine$', views.uploadPicture),
	#url(r'^ricinv/create$', views.RicognizioneInventarialeCreateView.as_view(),name='ricinv_add'),
	url(r'^ricinv/create$', views.ricognizioneInventarialeCreateView,name='ricinv_add'),
	url(r'^ricinv/edit/', views.ricognizioneInventarialeEditView,name='ricinv_edit'),
    url(r'^ricinv/delete/', views.ricognizioneInventarialeDeleteView,name='ricinv_delete'),
    url(r'^ricinv/getPossessori/$', views.getPossessori, name='getPossessori'),
	url(r'^ricinv$', views.ricinv, name='ricinv'),
    url(r'^table/getRicognizioniData', views.getRicognizioniData, name='getRicognizioniData'),
    url(r'^table/advancedRicognizioneInventarialeSearch$', views.advancedRicognizioneInventarialeSearch, name='advancedRicognizioneInventarialeSearch'),
    url(r'^esse3user-autocomplete/$', views.Esse3UserAutocomplete.as_view(), name='esse3user-autocomplete'),
    url(r'^update/esse3users', views.updateLocalEsse3Users, name='updateLocalEsse3Users'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
