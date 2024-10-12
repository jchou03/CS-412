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
    
    def get_status_messages(self):
        '''retrieve all status messages for this profile'''
        status_messages = StatusMessage.objects.filter(profile=self)
        return status_messages
    
class StatusMessage(models.Model):
    '''status message representing the current status of a profile'''
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField()
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    
    def __str__(self):
        '''string representation of a status message'''
        return f'{self.profile}: {self.message}'