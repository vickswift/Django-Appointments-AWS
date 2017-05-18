from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^appoint$', views.appoint),
    url(r'^add$', views.add),
    url(r'^update/(?P<appoint_id>\d+)$', views.update),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<appoint_id>\d+)$', views.delete),
    url(r'^edit_appoint/(?P<appoint_id>\d+)$', views.edit_appoint),
]
