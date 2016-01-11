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
#    # ex: /geomap/export_feedback
#    url(r'^export_feedback/$', views.export_feedback, name='export_feedback'),
#    # ex: /geomap/export_user
#    url(r'^export_user/$', views.export_user, name='export_user'),
]