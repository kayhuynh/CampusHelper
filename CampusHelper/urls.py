from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'CampusHelperApp.views.root'),
    # url(r'^frontend.css$',TemplateView.as_view(template_name='frontend.css'))
    url(r'^alltasks$', 'CampusHelperApp.views.alltasks'),
    url(r'^profile$', 'CampusHelperApp.views.profile'),
    url(r'^newtask$', 'CampusHelperApp.views.newtask'),
    url(r'^newuser$', 'CampusHelperApp.views.newuser'),
    url(r'^mytasks$', 'CampusHelperApp.views.mytasks'),
    url(r'^login$', 'CampusHelperApp.views.login')
)
