from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import Encubarte.plataforma.views

admin.autodiscover()

urlpatterns = patterns('Encubarte.plataforma.views',
    url(r'^admin/', include(admin.site.urls)),
    #Links publicos:
    url(r'^$', Encubarte.plataforma.views.inicioControl),
    url(r'^registro/$', Encubarte.plataforma.views.registroControl),
    url(r'^login/$', Encubarte.plataforma.views.loginControl),
    url(r'^logout/$', Encubarte.plataforma.views.logoutControl),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )