from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'django_getquery.demo.views.index', name = 'index'),
    url(r'^tester/$', 'django_getquery.demo.views.tester', name = 'tester'),
)
