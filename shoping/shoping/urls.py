from django.conf.urls import patterns, include, url
from django.contrib import admin
from shoping import settings

urlpatterns = patterns('',
                       # Examples:
                       url(r'', include('account.urls')),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT}),
)