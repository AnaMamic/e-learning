from django.contrib import admin
from .models import Course, Notification, Lesson, Institution,Subject
# Register your models here.

admin.site.register(Course)
admin.site.register(Institution)
admin.site.register(Subject)
admin.site.register(Lesson)