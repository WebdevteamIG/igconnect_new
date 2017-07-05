from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.projects,name='projects'),
	url(r'^addProject/$',views.addProject,name='addProject'),
	url(r'^editProject/(?P<projectname>[^/]+)/$',views.editProject,name='editProject'),
	url(r'^show/(?P<projectname>[^/]+)/$',views.show_project,name='show_project'),
]