from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'CampusHelperApp.views.root'),
    url(r'^alltasks$', 'CampusHelperApp.views.alltasks'),
    url(r'^profile$', 'CampusHelperApp.views.profile'),
    url(r'^task$', 'CampusHelperApp.views.task'),
    url(r'^newtask$', 'CampusHelperApp.views.newtask'),
    url(r'^newuser$', 'CampusHelperApp.views.newuser'),
    url(r'^mytasks$', 'CampusHelperApp.views.mytasks'),
    url(r'^login$', 'CampusHelperApp.views.login'),
    url(r'^logout$', 'CampusHelperApp.views.logout'),
    url(r'^newmessage$', 'CampusHelperApp.views.newmessage'),
    url(r'^mymessages$', 'CampusHelperApp.views.mymessages'),
    url(r'^verifyemail$', 'CampusHelperApp.views.verifyemail')
)
