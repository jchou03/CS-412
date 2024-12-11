# File: models.py
# Author: Jared Chou (jchou@bu.edu) 11/19/2024
# Description: Defining the different data models that represent different data in this app

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Trip(models.Model):
    '''a model that represents a trip'''
    name = models.TextField(blank=False) # the name of the trip
    
    # these fields can be blank upon creation 
    # because these may not be known when the trip is first created
    destination = models.TextField(blank=True, null=True) # string representation of destination
    start_date = models.DateField(blank=True, null=True) # start date of the trip
    end_date = models.DateField(blank=True, null=True) # end date of the trip
    
    def get_dates_string(self):
        '''get a string of the trip's start and end date in a readable format'''
        return f'{self.start_date.month}/{self.start_date.day}-{self.end_date.month}/{self.end_date.day}'
    
    def __str__(self):
        '''string representation of the model'''
        return f'Trip: {self.name} to {self.destination} ({self.get_dates_string()})'
    
    def get_attendees(self):
        '''get the attendees of this trip'''
        # use the AttendTrip object to access the many to many relationship
        # between Profile and Trip objects
        trip_attendees = AttendTrip.objects.filter(trip=self)
        # get the pks of each Profile attending the trip
        pks = [p.profile.pk for p in trip_attendees]
        # use the pks to get a list of Profile objects of people attending this trip
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
        '''Returns the url used to display this trip.
        This is used to display a trip once a new trip has been created
        '''
        return reverse("show_trip", kwargs={"pk": self.pk})
    
    
class Profile(models.Model):
    '''a model that represents a user of the app'''
    
    # relate each profile to a django User object to connect this model with django authentication
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="django_user")
    
    first_name = models.TextField(blank=False) # first name of user
    last_name = models.TextField(blank=False) # last name of user
    # phone number may be provided at a later date
    phone_number = models.BigIntegerField(blank=True, null=True) # phone number of user
    
    def __str__(self):
        '''string representation of the model'''
        return f'{self.first_name} {self.last_name}'
    
class Cost(models.Model):
    '''a model that represents a planned or actual cost of a given trip'''
    item_name = models.TextField(blank=False) # name of the item
    
    # (this number will be positive due to requirements in the form)
    item_price = models.FloatField(blank=False) # price of the item 
    
    # boolean representing whether or not this was a cost that was paid
    actual_cost = models.BooleanField(blank=False) 
    
    # Profile of the user that actually paid for this cost. 
    # This could be unset if the cost has not be paid
    paid_by = models.ForeignKey('Profile', 
                                on_delete=models.SET_DEFAULT, 
                                default=1, 
                                blank=True, 
                                null=True) # 
    
    # the trip that this cost is associated with
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    
    def __str__(self):
        '''string representation of the model'''
        return f'{self.item_name} - ${self.item_price}'
    
class Image(models.Model):
    '''a model that represents images that trip attendees can post to share with other attendees'''
    image = models.ImageField() # image data that is posted
    
    # the trip that this image is associated with
    trip = models.ForeignKey('Trip', on_delete=models.DO_NOTHING) 
    # the Profile that posted this image
    poster = models.ForeignKey('Profile', on_delete=models.SET_DEFAULT, default=1)
    
    def __str__(self):
        '''string representation of model'''
        return f'Image from {self.trip} posted by {self.poster}'
    
class AttendTrip(models.Model):
    '''a model representing a many to many relationship between the Trip and Profile models'''
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE) # trip attended
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE) # profile attending the trip
    
    def __str__(self):
        '''string representation of model'''
        return f'{self.profile} attended {self.trip}'
        