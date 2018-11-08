from django.conf.urls import url, include 
from django.contrib import admin
import authentication.views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^main$', authentication.views.igconnect),
    url(r'^$', authentication.views.home),
    url(r'^auth/', include('authentication.urls', namespace = 'authentication')),
    url(r'^projects/', include('projects.urls', namespace = 'projects')),
    url(r'^updates/',include('updates.urls', namespace = 'updates')),
    url(r'^borrow/',include('inventory.urls',namespace='inventory')),
    url(r'^events/',include('events.urls',namespace='events')),
    url(r'^exp/', include('experience.urls', namespace='experience')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^register/', include('register.urls', namespace='register')),

    #password reset views
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

