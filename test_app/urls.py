from django.conf.urls import patterns, include, url
from test_app.views import home, done, logout, error, deauth

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^deauth/$', deauth, name='deauth'),

    url(r'^admin/', include(admin.site.urls)),

    url('', include('social.apps.django_app.urls', namespace='social')),
)
