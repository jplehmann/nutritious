from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('tagz.views',

    # resources
    url(r'^tagz/lib/$', 'lib'),
    url(r'^tagz/lib/(?P<res_name>[^\/]+)/(?P<ref_str>[^\/]+)?$', 'render_resource'),

    # TAG REFERENCE
    # tag detail (GET, DEL)
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)/refs/(?P<id>\d+)$', 'tagref_detail'),
    # create form for specific tag
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)/refs/createform', 'tagref_createform'),
    # create form with arbitrary tag (create tag too)
    url(r'^tagz/tags/createform', 'tagref_createform'),
    # tag create (POST)
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)/refs$', 'tagref_create'),
    # what is this for?
    #url(r'^tagz/tags/(?P<tag_name>[^\/]+)/refs', 'tagref_create'),

    #url(r'^tagz/refs/(?P<ref_name>[^\/]+)/$', 'ref'),

    # TAGS
    # all tags
    url(r'^tagz/tags/$', 'tags'),
    # Export -- need more specific name o/w confusing
    # TODO: name these better
    url(r'^tagz/tags/export$', 'tags_export'),
    url(r'^tagz/tags/import$', 'tags_import'),
    # specific tag (GET, DEL)
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)', 'tag'),
    #url(r'^tagz/tags/(?P<tag_name>[^\/]+)/editform$', 'tag_edit'),

    # home
    url(r'^tagz/$', 'nasb'), # redir to tags
    url(r'^$', 'nasb'), # redir to tags

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    # login
    url(r'^tagz/accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    # logout
    url(r'^tagz/accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    #url(r'^tagz/accounts/logout/$', 'tagz.views.logout')

  (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'})
    
)

