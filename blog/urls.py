from django.conf.urls import patterns, url
from .views import (IndexView, EntryDetailView)

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^entry/(?P<slug>[\w-]+)/$', EntryDetailView.as_view(),
        name='entry-detail')
)
