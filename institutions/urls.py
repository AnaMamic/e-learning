from django.conf.urls import url

from . import views


app_name='institutions'
urlpatterns = [
    
	
    url(r'^add/(?P<course_slug>[a-zA-Z0-9-]+)/$', views.add_institution, name='add_institution'),
	url(r'^add/$', views.add_institution, name='add_institution'),
	url(r'^(?P<institution_slug>[a-zA-Z0-9-]+)/$', views.institution_courses, name='institution_courses'),
	
]

