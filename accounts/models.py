from django.db import models
from django.contrib.auth.models import User
from map.models import location
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    loaction = models.ForeignKey(location, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.username