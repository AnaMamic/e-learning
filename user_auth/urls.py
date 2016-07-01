from django.conf.urls import url
from . import views

app_name = 'user_auth'
urlpatterns = [
	url(r'^register/$', views.CustomUserRegistration, name='register'),
    url(r'^login/$', views.LoginRequest, name='login'),
    url(r'^logout/$', views.LogoutRequest, name='logout'),
   ]