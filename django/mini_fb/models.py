from django.db import models
from django.urls import reverse

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
    
    def get_absolute_url(self):
        '''get absolute url for profile after creating a new profile'''
        # print("getting absolute url")
        return reverse("show_profile", kwargs={"pk": self.pk})
    
    def get_friends(self):
        '''get a list of all friends of this profile'''
        friendships = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)
        friends = []
        for f in friendships:
            if f.profile1==self:
                friends.append(f.profile2)
            else:
                friends.append(f.profile1)
        # print(f'{self} has these friends: {friends}')
        return friends
    
class StatusMessage(models.Model):
    '''status message representing the current status of a profile'''
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField()
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    
    def __str__(self):
        '''string representation of a status message'''
        return f'{self.profile}: {self.message}'
    
    def get_images(self):
        '''get the images associated with this status message'''
        images = Image.objects.filter(statusMessage=self)
        return images
    
class Image(models.Model):
    '''model representing an image to be displayed on a user's profile'''
    image = models.ImageField(blank=True)
    statusMessage = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.statusMessage} : {self.image}'
    
class Friend(models.Model):
    '''model representing a friend relationship between two profiles'''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.profile1} & {self.profile2}'
    
    
    