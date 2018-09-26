from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.eventsHome,name='eventsHome'),
	url(r'^(?P<id>[0-9]+)/$',views.viewEvent,name='viewEvent'),
	url(r'^register/(?P<id>[0-9]+)/$',views.registerEvent,name='registerEvent'),
	url(r'^addevent/$',views.addEvent,name='addEvent'),
	url(r'^manageevent/(?P<id>[0-9]+)/$',views.manageEvent,name='manageEvent'),
	url(r'^manageevent/responses/(?P<id>[0-9]+)/$',views.viewResponses,name='responses'),
	url(r'^editevent/(?P<id>[0-9]+)/$',views.editEvent,name='editEvent'),
	url(r'^addQuestion/(?P<id>[0-9]+)/$',views.addQuestion,name='addQuestion'),
	url(r'^getresponse/$',views.getResponse,name='getResponse'),
	url(r'^updateresponse/$',views.updateRegRequest,name='updateRegRequest'),
	url(r'^downloadresponse/(?P<id>[0-9]+)/$',views.downloadResponses,name='downloadResponses'),
	#award
	url(r'^spura/$',views.spura,name='spura'),
	url(r'^register/spura/$',views.registerspura,name='spura'),

]