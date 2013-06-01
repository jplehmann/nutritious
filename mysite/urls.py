from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

  # home
  url(r'^$', view=direct_to_template, kwargs={'template': 'home.html'},
      name="home"), 

  # admin
  url(r'^admin/', include(admin.site.urls)),

  # login
  url(r'^accounts/login/$', 
      view=login, kwargs={'template_name': 'accounts/login.html'}, 
      name='login'),

  # logout
  url(r'^accounts/logout/$', view=logout_then_login, 
      name='logout'),

  (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', 
          {'url': '/static/img/favicon.ico'})
)

urlpatterns += patterns('tags.views',

  # Tag References

  # tag detail (GET, DEL)
  url(r'^tags/(?P<tag_name>[^\/]+)/refs/(?P<id>\d+)$', view='tagref_detail',
      name='tagref_detail'),

  # create form for specific tag
  url(r'^tags/(?P<tag_name>[^\/]+)/refs/createform', view='tagref_createform', 
      name='create_tagref_for_tag'),

  # create form with arbitrary tag (create tag too)
  url(r'^tags/createform', view='tagref_createform', 
      name='create_tagref'),

  # tag create (POST)
  url(r'^tags/(?P<tag_name>[^\/]+)/refs$', view='tagref_create', 
      name='post_tagref'),


  # Tags

  # all tags
  url(r'^tags/$', view='tags', name='tags'),

  # Export -- need more specific name o/w confusing
  url(r'^tags/export$', view='tags_export', name='tags_export'),
  url(r'^tags/import$', view='tags_import', name='tags_import'),

  # specific tag (GET, DEL)
  url(r'^tags/(?P<tag_name>[^\/]+)', view='tag', name='tag'),

)

urlpatterns += patterns('texts.views',

  # Text resources

  # library
  url(r'^texts/$', view='lib', name="library"),

  # references
  url(r'^texts/(?P<res_name>[^\/]+)/(?P<ref_str>[^\/]+)?$', 
      view='get_resource', 
      name='resource'),

)


