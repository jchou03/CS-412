from django.db import models

# Create your models here.
class Trip(models.Model):
    '''a model that represents a trip'''
    name = models.TextField(blank=False)
    # these fields can be blank upon creation because these may not be set in stone when the trip is first created
    destination = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        '''string representation of the model'''
        return f'Trip: {self.name} to {self.destination} ({self.start_date.month}/{self.start_date.day}-{self.end_date.month}/{self.end_date.day})'
    
class Profile(models.Model):
    '''a model that represents a user of the app'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    # phone number may be provided at a later date
    phone_number = models.BigIntegerField(blank=True, null=True)
    
    def __str__(self):
        '''string representation of the model'''
        return f'{self.first_name} {self.last_name}'
    
class Cost(models.Model):
    '''a model that represents a planned or actual cost of the upcoming trip'''
    item_name = models.TextField(blank=False)
    item_price = models.FloatField(blank=False)
    actual_cost = models.BooleanField(blank=False)
    paid_by = models.ForeignKey('Profile', on_delete=models.SET_DEFAULT, default=1)
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
        