from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    def __str__(self):
        return self.user.username
    
class user_current_location(models.Model):
    user =models.OneToOneField(UserProfile, on_delete=models.CASCADE) 
    current_location = models.CharField(max_length=400 , null=True , blank= True)

