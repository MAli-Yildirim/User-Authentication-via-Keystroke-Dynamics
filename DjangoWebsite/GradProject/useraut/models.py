from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.



class Data(models.Model):
    content = models.JSONField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.TextField(default=None)