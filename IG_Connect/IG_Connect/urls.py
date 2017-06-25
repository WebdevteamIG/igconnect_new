from django.conf.urls import url, include 
from django.contrib import admin
import authentication.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', authentication.views.index),
    url(r'^index/', authentication.views.index),
    url(r'^auth/', include('authentication.urls', namespace = 'authentication')),
    url(r'^projects/', include('projects.urls', namespace = 'projects'))
]

