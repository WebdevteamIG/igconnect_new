from django.conf.urls import url, include 
from django.contrib import admin
import authentication.views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', authentication.views.index),
    url(r'^auth/', include('authentication.urls', namespace = 'authentication')),
    url(r'^projects/', include('projects.urls', namespace = 'projects')),
    url(r'^updates/',include('updates.urls', namespace = 'updates')),
    url(r'^borrow/',include('inventory.urls',namespace='inventory')),
    url(r'^events/',include('events.urls',namespace='events')),
    url(r'^exp/', include('experience.urls', namespace='experience')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

