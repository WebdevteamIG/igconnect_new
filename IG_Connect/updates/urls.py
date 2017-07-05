from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.dashboard,name='dashboard'),
	url(r'^addNews/$',views.addNews,name='addNews'),
	url(r'^publish/((?P<id>[0-9]+))/$',views.publishNews,name='publishNews'),
	url(r'^unpublish/((?P<id>[0-9]+))/$',views.unPublishNews,name='unPublishNews'),
]