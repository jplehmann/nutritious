from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tagz.views.home', name='home'),
    url(r'^tagz/$', 'tagz.views.tags'), # redir to tags
    url(r'^tagz/tags/$', 'tagz.views.tags'),
    url(r'^tagz/refs/$', 'tagz.views.refs'),
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)/$', 'tagz.views.tag'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
