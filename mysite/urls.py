from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('tagz.views',
    # resources
    url(r'^res/$', view='lib', name="library"),
    url(r'^res/(?P<res_name>[^\/]+)/(?P<ref_str>[^\/]+)?$', view='get_resource', name='resource'),

    # TAG REFERENCE
    # tag detail (GET, DEL)
    url(r'^tags/(?P<tag_name>[^\/]+)/refs/(?P<id>\d+)$', view='tagref_detail', name='tagref_detail'),
    # create form for specific tag
    url(r'^tags/(?P<tag_name>[^\/]+)/refs/createform', view='tagref_createform', name='create_tagref_for_tag'),
    # create form with arbitrary tag (create tag too)
    url(r'^tags/createform', view='tagref_createform', name='create_tagref'),
    # tag create (POST)
    url(r'^tags/(?P<tag_name>[^\/]+)/refs$', view='tagref_create', name='post_tagref'),
    # what is this for?
    #url(r'^tags/(?P<tag_name>[^\/]+)/refs', 'tagref_create'),

    #url(r'^refs/(?P<ref_name>[^\/]+)/$', 'ref'),

    # TAGS
    # all tags
    url(r'^tags/$', view='tags', name='tags'),
    # Export -- need more specific name o/w confusing
    # TODO: name these better
    url(r'^tags/export$', view='tags_export', name='tags_export'),
    url(r'^tags/import$', view='tags_import', name='tags_import'),
    # specific tag (GET, DEL)
    url(r'^tags/(?P<tag_name>[^\/]+)', view='tag', name='tag'),
    #url(r'^tags/(?P<tag_name>[^\/]+)/editform$', 'tag_edit'),

    # home
    url(r'^$', view=direct_to_template, 
      kwargs={'template': 'home.html'}, name="home"), # redir to tags

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    # login
    url(r'^accounts/login/$', view=login, 
      kwargs={'template_name': 'accounts/login.html'}, name='login'),
    # logout
    url(r'^accounts/logout/$', view=logout_then_login, name='logout'),
    #url(r'^accounts/logout/$', 'tagz.views.logout')

  (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'})
    
)

