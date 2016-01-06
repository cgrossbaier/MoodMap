from django.conf.urls import url

from . import views

app_name = 'geomap'

urlpatterns = [
    # ex: /geomap/
    url(r'^$', views.index, name='index'),
    # ex: /geomap/loginUser
    url(r'^loginUser/$', views.loginUser, name='loginUser'),
    # ex: /geomap/
    url(r'^logoutUser/$', views.logoutUser, name='logoutUser'),
    # ex: /geomap/5/
    url(r'^(?P<map_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /geomap/5/addChoice/
    url(r'^(?P<map_id>[0-9]+)/addChoice/$', views.addChoice, name='addChoice'),
    # ex: /geomap/5/changeMap/
    url(r'^(?P<map_id>[0-9]+)/changeMap/$', views.changeMap, name='changeMap'),
    # ex: /geomap/5/changeChoice/
    url(r'^(?P<map_id>[0-9]+)/changeChoice/$', views.changeChoice, name='changeChoice'),
]