from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('tagz.views',
    # resources
    url(r'^tagz/lib/$', view='lib', name="library"),
    url(r'^tagz/lib/(?P<res_name>[^\/]+)/(?P<ref_str>[^\/]+)?$', view='get_resource', name='resource'),

    # TAG REFERENCE
    # tag detail (GET, DEL)
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)/refs/(?P<id>\d+)$', view='tagref_detail', name='tagref_detail'),
    # create form for specific tag
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)/refs/createform', view='tagref_createform', name='create_tagref_for_tag'),
    # create form with arbitrary tag (create tag too)
    url(r'^tagz/tags/createform', view='tagref_createform', name='create_tagref'),
    # tag create (POST)
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)/refs$', view='tagref_create', name='post_tagref'),
    # what is this for?
    #url(r'^tagz/tags/(?P<tag_name>[^\/]+)/refs', 'tagref_create'),

    #url(r'^tagz/refs/(?P<ref_name>[^\/]+)/$', 'ref'),

    # TAGS
    # all tags
    url(r'^tagz/tags/$', view='tags', name='tags'),
    # Export -- need more specific name o/w confusing
    # TODO: name these better
    url(r'^tagz/tags/export$', view='tags_export', name='tags_export'),
    url(r'^tagz/tags/import$', view='tags_import', name='tags_import'),
    # specific tag (GET, DEL)
    url(r'^tagz/tags/(?P<tag_name>[^\/]+)', view='tag', name='tag'),
    #url(r'^tagz/tags/(?P<tag_name>[^\/]+)/editform$', 'tag_edit'),

    # home
    url(r'^tagz/$', view='nasb', name="home"), # redir to tags
    url(r'^$', view='nasb', name="index"), # redir to tags

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    # login
    url(r'^tagz/accounts/login/$', view='django.contrib.auth.views.login', kwargs={'template_name': 'accounts/login.html'}, name='login'),
    # logout
    url(r'^tagz/accounts/logout/$', view='django.contrib.auth.views.logout_then_login', name='logout'),
    #url(r'^tagz/accounts/logout/$', 'tagz.views.logout')

  (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'})
    
)

