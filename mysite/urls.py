from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('tagz.views',
    # Examples:
    url(r'^tagz/lib/$', 'lib'),
    url(r'^tagz/lib/(?P<res_name>[^\/]+)/(?P<ref_str>[^\/]+)?$', 
          'lib_resource'),
    url(r'^tagz/tags/$', 'tags'),
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)/$', 'tag'),
    url(r'^tagz/refs/$', 'tagz.views.refs'),
    url(r'^tagz/refs/(?P<ref_name>[^\/]+)/$', 'ref'),
    # home
    url(r'^tagz/$', 'nasb'), # redir to tags
    url(r'^$', 'nasb'), # redir to tags

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
