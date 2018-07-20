from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^add_exp$', views.add_exp, name='add_exp'),
]
