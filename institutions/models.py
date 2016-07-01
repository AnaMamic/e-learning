from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Institution(models.Model):
	name= models.CharField(max_length=100);
	slug = models.SlugField(unique=True)
	
	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']



