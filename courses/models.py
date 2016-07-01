from __future__ import unicode_literals
from django.db import models
from subjects.models import Subject
from institutions.models import Institution
from django.db.models.signals import pre_save,pre_delete
from django.db.models import Q
import os

def content_file_name(instance, filename):
    return '/'.join(['pdf_files', instance.lesson.chapter.course.slug,instance.lesson.chapter.slug,instance.lesson.slug, filename])

class Course(models.Model):
	professor = models.ForeignKey("auth.User", limit_choices_to={'groups__name': "professor"})
	student = models.ManyToManyField("auth.User", limit_choices_to={'groups__name': "student"},related_name='student',blank=True)
	slug = models.SlugField(unique=True)
	institution = models.ForeignKey(Institution,on_delete=models.CASCADE)
	subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	description = models.TextField()
	image = models.ImageField(upload_to="course_img/")
	
	def __str__(self):
		return self.name


	



class Notification(models.Model):
	course= models.ForeignKey(Course,on_delete=models.CASCADE)
	slug = models.SlugField(unique=True)
	name= models.CharField(max_length=100)
	text= models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-modified']



class Chapter(models.Model):
	
	course= models.ForeignKey(Course,on_delete=models.CASCADE)
	slug = models.SlugField(unique=True)
	name = models.CharField(max_length=100)
	class Meta:
		ordering = ['pk']


	def __str__(self):
		return self.name


class Lesson(models.Model):
	chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
	slug = models.SlugField(unique=True)
	name = models.CharField(max_length=100)
	text = models.TextField(blank=True, null=True)
	video_link = models.CharField(max_length=300, blank=True, null=True)

	class Meta:
		ordering = ['pk']

	
	def __str__(self):
		return self.name


class LessonFile(models.Model):
	lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
	pdf_file= models.FileField(upload_to=content_file_name)
	slug = models.SlugField(unique=True)
	

	def __str__(self):
		return self.pdf_file.name.split('/')[4]




def pre_save_make_slug(sender,instance,*args,**kwargs):
	if instance.slug == "":
		if sender==LessonFile:
			slug = instance.pdf_file.name.replace(" ","").lower()
		else:
			slug = instance.name.replace(" ","").lower()
		reg = slug+r"-[0-9]+/$" 

		count = sender.objects.filter(Q(slug=slug) | Q(slug=reg)).count()
		
		if count != 0:
			slug = "%s-%s" %(slug,count)

		instance.slug=slug
	if sender==Course:
		try:
			thisobject = Course.objects.get(pk=instance.id)
			if thisobject.image != instance.image:
				thisobject.image.delete(False)
		except: pass
	




def delete_file(sender,instance,*args,**kwargs):
	if sender==LessonFile:
		instance.pdf_file.delete(False)
	else:
		instance.image.delete(False)


pre_save.connect(pre_save_make_slug,sender=Course)
pre_save.connect(pre_save_make_slug,sender=Chapter)
pre_save.connect(pre_save_make_slug,sender=Notification)
pre_save.connect(pre_save_make_slug,sender=Lesson)
pre_save.connect(pre_save_make_slug,sender=Institution)
pre_save.connect(pre_save_make_slug,sender=Subject)
pre_save.connect(pre_save_make_slug,sender=LessonFile)

pre_delete.connect(delete_file,sender=Course)
pre_delete.connect(delete_file,sender=LessonFile)



