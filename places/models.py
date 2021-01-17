import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Place(models.Model):
    class PlaceAttributes(models.TextChoices):
        AMBIANCE = 'AMB', _('Ambiance')
        ATMOSPHERE = 'ATMS', _('Atmosphere')
        CLEANLINESS = 'CLN', _('Cleanliness')
        DRINK = 'DNK', _('Drink')
        ENTERTAINMENT = 'ENT', _('Entertainment')
        FOOD = 'FD', _('Food')
        QUALITY = 'QLTY', _('Quality')
        SERVICE = 'SRV', _('Service')
        SPEED = 'SPD', _('Speed')
        VALUE = 'VAL', _('Value')

    name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    suburb = models.CharField(max_length=50)
    state = models.CharField(max_length=3)
    postcode = models.CharField(max_length=4)

    def __str__(self):
        return self.name + ', ' + self.suburb



class Review(models.Model):
    """
    Stores a feedback for a select few of defined place attributes
    """
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    positive_feedback = ArrayField(
        models.CharField(choices=Place.PlaceAttributes.choices, max_length=4),
        blank=True,
        null=True
    )
    negative_feedback = ArrayField(
        models.CharField(choices=Place.PlaceAttributes.choices, max_length=4),
        blank=True,
        null=True
    )

class Review_Record(models.Model):
    """
    Maintains an updated score of each possible place attribute
    """
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    scores = models.JSONField(default=dict)
