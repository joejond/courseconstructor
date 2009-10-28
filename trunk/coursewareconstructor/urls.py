from django.conf.urls.defaults import *
from course_manager import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^coursewareconstructor/', include('coursewareconstructor.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    (r'^admin/', include(admin.site.urls)),
    (r'^cw/$', views.index),
    (r'^cw/course/(?P<slug>.{0,10})\.html$', views.show_course),
    (r'^cw/section/(?P<slug>.{0,10})\.html$', views.show_section),
    (r'^[.]{0}$', views.home),

)
