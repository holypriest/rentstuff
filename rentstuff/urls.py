from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.Login, name='login'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^register/$', views.register, name='cadastro'),
    url(r'^ad/$', views.ad, name='anuncio'),
    url(r'^aluguel/(?P<ad_id>[0-9]+)/$', views.aluguel, name='aluguel'),
    url(r'^sucesso/$', views.sucesso, name='sucesso'),
    url(r'^categoria/(?P<cat>.*)/$', views.categoria, name='categoria'),
    url(r'anuncios/(?P<anuncio_id>[0-9]+)/$', views.detalhes, name='detalhes'),
    url(r'usuarios/(?P<usr>[a-z_.]+)/$', views.usuario, name='usuario'),
]
