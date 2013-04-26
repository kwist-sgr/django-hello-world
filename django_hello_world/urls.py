from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django_hello_world.hello.views import ProfileEditView


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'django_hello_world.hello.views.home', name='home'),
    #url(r'^django_hello_world/', include('django_hello_world.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + '/js'}),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + '/css'}),
    url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + '/photos'}),

    url(r'^requests/?$', 'django_hello_world.hello.views.requests', name='requests'),
    url(r'^profile/(?P<pk>\d+)/edit/?$', ProfileEditView.as_view(), name='profile_edit'),
)
