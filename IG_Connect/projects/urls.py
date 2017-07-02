from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.projects,name='projects'),
	url(r'^show_project/$',views.show_project,name='show_project'),
]