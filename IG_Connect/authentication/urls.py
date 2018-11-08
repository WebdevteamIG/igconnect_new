from django.conf.urls import url
import views

urlpatterns = [
    # url(r'^$', views.index, name = 'index'),
    
    url(r'^login/', views.signin, name = 'login'),
    url(r'^signup/', views.signup, name = 'signup'),
    url(r'^logout/', views.signout, name = 'logout'),
    url(r'^register/', views.register, name = 'register'),
    url(r'^profile/(?P<regNum>[^/]+)/$',views.profile,name='profile'),
    url(r'^forgotPassword/$',views.forgotPassword,name='forgotPassword'),
    url(r'^updateProfile/$',views.updateProfile,name="updateProfile"),
    url(r'^webteam/$',views.webteam,name='webteam'),
    url(r'^contactUs/$',views.contactUs,name='contactUs'),
]