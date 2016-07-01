from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
        user            = models.OneToOneField(User)
        last_name       = models.CharField(max_length=20, blank=False)
        first_name      = models.CharField(max_length=20, blank=False)
        ### koristi se pri prijavi da se mogu razlikovati korisnici 
        professor       = models.BooleanField(default=False)

        def __unicode__(self):
                return (self.first_name + '' + self.last_name)