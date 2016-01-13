from django.conf.urls import url

from . import views

app_name = 'geomap'

urlpatterns = [
    # ex: /geomap/
    url(r'^$', views.index, name='index'),
    # ex: /geomap/
    url(r'^map/$', views.mapView, name='mapView'),
    # ex: /geomap/
    url(r'^checkVerification/$', views.checkVerification, name='checkVerification'),
    # ex: /addEvent
    url(r'^addEvent/$', views.addEvent, name='addEvent'),
    # ex: /searchQuery
    url(r'^searchQuery/$', views.searchQuery, name='searchQuery'),
    # ex: /saveStatistics
    url(r'^saveStatistics/$', views.saveStatistics, name='saveStatistics'),
    # ex: /geomap/export_stats
    url(r'^export_stats/$', views.export_stats, name='export_stats'),
#    # ex: /geomap/export_user
#    url(r'^export_user/$', views.export_user, name='export_user'),
]