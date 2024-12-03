from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Trip(models.Model):
    '''a model that represents a trip'''
    name = models.TextField(blank=False)
    # these fields can be blank upon creation because these may not be set in stone when the trip is first created
    destination = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    def get_dates_string(self):
        '''get a string of the trip's start and end date'''
        return f'{self.start_date.month}/{self.start_date.day}-{self.end_date.month}/{self.end_date.day}'
    
    def __str__(self):
        '''string representation of the model'''
        return f'Trip: {self.name} to {self.destination} ({self.get_dates_string()})'
    
    def get_attendees(self):
        '''get the attendees of this trip'''
        trip_attendees = AttendTrip.objects.filter(trip=self)
        pks = [p.profile.pk for p in trip_attendees]
        attendees = Profile.objects.filter(pk__in=pks)
        return attendees
    
    def get_costs(self):
        '''get the costs associated with this trip'''
        costs = Cost.objects.filter(trip=self)
        return costs
        
    def get_images(self):
        '''get the images associated with this trip'''
        images = Image.objects.filter(trip=self)
        return images
    
    def get_absolute_url(self):
        '''display a trip once a new trip has been created'''
        return reverse("show_trip", kwargs={"pk": self.pk})
    
    
class Profile(models.Model):
    '''a model that represents a user of the app'''
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="django_user")
    
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    # phone number may be provided at a later date
    phone_number = models.BigIntegerField(blank=True, null=True)
    
    def __str__(self):
        '''string representation of the model'''
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        '''get absolute url to display the profile after creating a new one'''
        
    
class Cost(models.Model):
    '''a model that represents a planned or actual cost of the upcoming trip'''
    item_name = models.TextField(blank=False)
    item_price = models.FloatField(blank=False)
    actual_cost = models.BooleanField(blank=False)
    paid_by = models.ForeignKey('Profile', on_delete=models.SET_DEFAULT, default=1, blank=True, null=True)
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    
    def __str__(self):
        '''string representation of the model'''
        return f'{self.item_name} - ${self.item_price}'
    
class Image(models.Model):
    '''a model that represents images that trip attendees can post to share with other attendees'''
    image = models.ImageField()
    trip = models.ForeignKey('Trip', on_delete=models.DO_NOTHING)
    poster = models.ForeignKey('Profile', on_delete=models.SET_DEFAULT, default=1)
    
    def __str__(self):
        '''string representation of model'''
        return f'Image from {self.trip} posted by {self.poster}'
    
class AttendTrip(models.Model):
    '''a model representing a many to many relationship between the Trip and Profile models'''
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    
    def __str__(self):
        '''string representation of model'''
        return f'{self.profile} attended {self.trip}'
        