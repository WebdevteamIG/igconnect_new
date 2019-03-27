from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^buynow/$', views.buynow),
	url(r'^lend/$', views.lend),
	url(r'^lended/$', views.lendedComponents),
	url(r'^admin/$', views.admin),
	url(r'^return_item/$',views.return_item),
]	