from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^tagz/lib/$', 'tagz.views.lib'),
    url(r'^tagz/lib/(?P<res_name>[^\/]+)/(?P<ref_str>[^\/]+)?$', 
          'tagz.views.lib_resource'),
    url(r'^tagz/tags/$', 'tagz.views.tags'),
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)/$', 'tagz.views.tag'),
    url(r'^tagz/refs/$', 'tagz.views.refs'),
    url(r'^tagz/refs/(?P<ref_name>[^\/]+)/$', 'tagz.views.ref'),
    # home
    url(r'^tagz/$', 'tagz.views.nasb'), # redir to tags
    url(r'^$', 'tagz.views.tags'), # redir to tags

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
