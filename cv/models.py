from django.conf import settings
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField



class CV(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    details = HTMLField()
    profile = HTMLField()
    education = HTMLField()
    technical_skills = HTMLField()
    experience = HTMLField()
    
    def publish(self):
        #self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
