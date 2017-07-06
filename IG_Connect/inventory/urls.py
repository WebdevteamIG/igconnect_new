from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.listItems,name='listItems'),
	url(r'^requestItem/(?P<id>[0-9]+)/$',views.requestItem,name='requestItem'),
	url(r'^cancelItemRequest/(?P<id>[0-9]+)/$',views.cancelItemRequest,name='cancelItemRequest'),
	url(r'^getItemBack/(?P<id>[0-9]+)/(?P<Actiontype>[0-9]+)/$',views.getItemBack,name='getItemBack'),
	url(r'^approve/(?P<id>[0-9]+)/$',views.approveItemRequest,name='approveItemRequest'),
	url(r'^addItem/$',views.addItem,name='addItem'),
	url(r'^listRequests/$',views.listRequests,name='listRequests'),
	url(r'^viewLogs/$',views.viewLogs,name='viewLogs'),
]