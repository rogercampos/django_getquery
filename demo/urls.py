from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'get_query_example.demo.views.index', name = 'index'),
    url(r'^tester/$', 'get_query_example.demo.views.tester', name = 'tester'),
)
