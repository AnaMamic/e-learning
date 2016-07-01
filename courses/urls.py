from django.conf.urls import url

from . import views


app_name='courses'
urlpatterns = [
    url(r'^$', views.index, name='all_courses'),
    

    
    url(r'^my/$',views.my_courses,name='my_courses'), 
    url(r'^my/create/$', views.create_edit_course, name='create'), 
    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/$',views.course_detail,name='course_detail'), 
    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/edit/$',views.create_edit_course, name='edit_course'),
    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/delete/$',views.delete_course, name='delete_course'),

    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/add-notification/$', views.create_edit_notification, name='add_notification' ),
    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<notification_slug>[a-zA-Z0-9-]+)/edit-notification/$', views.create_edit_notification, name='edit_notification' ), 
    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<notification_slug>[a-zA-Z0-9-]+)/delete-notification/$', views.delete_notification, name='delete_notification' ), 


    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/add-chapter/$', views.add_edit_chapter, name='add_chapter' ), 
    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<chapter_slug>[a-zA-Z0-9-]+)/edit-chapter/$', views.add_edit_chapter, name='edit_chapter'),
    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<chapter_slug>[a-zA-Z0-9-]+)/delete-chapter/$', views.delete_chapter, name='delete_chapter'),

    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<chapter_slug>[a-zA-Z0-9-]+)/add-lesson/$', views.add_edit_lesson, name='add_lesson'), 
    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<chapter_slug>[a-zA-Z0-9-]+)/(?P<lesson_slug>[a-zA-Z0-9-]+)/edit-lesson/$', views.add_edit_lesson, name='edit_lesson'), 
    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<chapter_slug>[a-zA-Z0-9-]+)/(?P<lesson_slug>[a-zA-Z0-9-]+)/delete-lesson/$', views.delete_lesson, name='delete_lesson'), 
    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<chapter_slug>[a-zA-Z0-9-]+)/(?P<lesson_slug>[a-zA-Z0-9-]+)/$', views.lesson_detail, name='lesson'),



    

    url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/student/$',views.course_student,name='course_student'),

    url(r'^(?P<course_slug>[a-zA-Z0-9-]+)/$', views.course_description, name='course_description'), 
    
     url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<chapter_slug>[a-zA-Z0-9-]+)/(?P<lesson_slug>[a-zA-Z0-9-]+)/add-file/$', views.add_file, name='add_file'), 
      url(r'^my/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<chapter_slug>[a-zA-Z0-9-]+)/(?P<lesson_slug>[a-zA-Z0-9-]+)/(?P<file_slug>[a-zA-Z0-9-._]+)/delete-file/$', views.delete_file, name='delete_pdf_file'), 

]