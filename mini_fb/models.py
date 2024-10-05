from django.db import models

# Create your models here.
class Profile(models.Model):
    '''information about user profiles for our mini_fb application'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_image_url = models.TextField(blank=True)
    
    def __str__(self):
        '''string representation of profile objects'''
        return self.first_name + " " + self.last_name