from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^z/', include('adm.urls', namespace='adm')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^comments/', include('django_comments.urls', namespace='comments')),
    url(r'^admin/', include(admin.site.urls)),
)
