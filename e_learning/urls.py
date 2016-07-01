"""e_learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$','courses.views.home'),
    url(r'^about/', 'courses.views.about'),
    url(r'^contact/', 'courses.views.contact'),
    url('^', include('django.contrib.auth.urls')),
    
    url(r'^admin/', admin.site.urls),
    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^courses/', include('courses.urls')),
    url(r'^subjects/', include('subjects.urls')),
    url(r'^institutions/', include('institutions.urls')),
    url(r'^user_auth/', include('user_auth.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^media/pdf_files/(?P<course_slug>[a-zA-Z0-9-]+)/(?P<chapter_slug>[a-zA-Z0-9-]+)/(?P<lesson_slug>[a-zA-Z0-9-]+)/(?P<file_slug>[a-zA-Z0-9-._]+)$','courses.views.show_pdf_file'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)

