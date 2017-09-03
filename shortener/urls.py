from django.conf.urls import patterns, include, url
from short_urls import views

# no admin section needed
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shortener.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^shorten', views.shorten, name='shorten'),
    # URL suffix can be in the Base62 range
    url(r'^[a-zA-Z0-9]+$', views.redirect_to_long, name='redirect_to_long'),
)
