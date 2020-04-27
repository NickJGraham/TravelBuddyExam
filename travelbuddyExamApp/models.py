from django.db import models
import re
from datetime import datetime, time, date
from time import strftime

PW_REGEX = re.compile(r'(?=.*\d).{8,}')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['firstname'] = 'Name must be at least 3 characters.'
        if len(postData['username']) < 3:
            errors['username_length'] = 'Username must be at least 3 characters.'
        if not PW_REGEX.match(postData['password']):
            errors['password_match'] = "Password is invalid!"
        if postData['password'] != postData['conf_password']:
            errors['passconf'] = "Password's Don't Match!"
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        d = datetime.now()
        now = d.strftime("%Y-%m-%d")
        if len(postData['destination']) < 1:
            errors['destination'] = "Destination field is required."
        if len(postData['description']) < 1:
            errors['description'] = "Description field is required."
        try:
            str(datetime.strptime(postData["dateFrom"], "%Y-%m-%d"))
        except ValueError:
            errors['datetime'] = "Invalid date. Please input a date."
        if str(date.today()) > str(postData['dateFrom']):
            errors['dateFrom'] = "Start time cannot be in the past."
        if str(date.today()) > str(postData['dateTo']):
            errors['dateTo'] = "End Date must be in the future."
        if postData['dateFrom'] > postData['dateTo']:
            errors['date'] = "Travel date 'to' cannot be before travel date 'from'."
        print(errors)
        return errors



class User(models.Model):
    name = models.CharField(max_length = 255)
    username= models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    startDate = models.CharField(max_length = 255)
    endDate = models.CharField(max_length = 255)
    plan = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tripMembers = models.ManyToManyField(User, related_name = 'joinedTrips')
    createdBy = models.ForeignKey(User, related_name='createdTrips', on_delete = models.CASCADE)
    objects = TripManager()