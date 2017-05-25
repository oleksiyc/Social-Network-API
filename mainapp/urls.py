from django.conf.urls import url

from mainapp import views

urlpatterns = [
	# main page
    url(r'^$', views.index, name='index'),
    # signup page
    url(r'^signup/$', views.signup, name='signup'),
    # register new user
	url(r'^register/$', views.register, name='register'),
    # login page
    url(r'^login/$', views.login, name='login'),
    # logout page
    url(r'^logout/$', views.logout, name='logout'),
    # members page
               url(r'^members/$', views.members, name='members'),
    # friends page
    url(r'^friends/$', views.friends, name='friends'),
    # user profile edit page
    url(r'^profile/$', views.profile, name='profile'),
    # messages page
               url(r'^messages/$', views.messages, name='messages'),
    # Ajax: check if user exists on registration page
    url(r'^regcheckuser/$', views.regCheckUser, name='regCheckUser'),
    # Ajax: check if user exists on login page
    url(r'^logcheckuser/$', views.logCheckUser, name='logCheckUser'),
]


