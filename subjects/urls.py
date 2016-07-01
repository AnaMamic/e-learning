from django.conf.urls import url

from . import views


app_name='subjects'
urlpatterns = [
    

    url(r'^add/(?P<course_slug>[a-zA-Z0-9-]+)/$', views.add_subject, name='add_subject'),
	url(r'^add/$', views.add_subject, name='add_subject'),
	url(r'^(?P<subject_slug>[a-zA-Z0-9-]+)/$', views.subject_courses, name='subject_courses'),
]