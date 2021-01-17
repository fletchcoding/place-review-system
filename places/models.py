import datetime

from django.db import models
from django.utils import timezone

class Place(models.Model):
    name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    suburb = models.CharField(max_length=50)
    state = models.CharField(max_length=3)
    postcode = models.CharField(max_length=4)

    def __str__(self):
        return self.name + ', ' + self.suburb

class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    ratings = models.JSONField(default=dict)
    pub_date = timezone.now()

class Review_Record(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    scores = models.JSONField(default=dict)
    """
    JSON FIELDS:
    Ambiance
    Atmosphere
    Cleanliness
    Drink
    Entertainment
    Food
    Quality
    Service
    Speed
    Value
    """
