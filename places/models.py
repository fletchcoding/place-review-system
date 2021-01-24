import datetime

from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

class Place(models.Model):
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
    visit_date = models.DateTimeField('Visit date and time', default=timezone.now())

    def __str__(self):
        return str(self.place) + ' for ' + str(self.visit_date) + ', by ' + str(self.reviewer.username)

class Feedback(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    atmosphere = models.BooleanField(null=True)
    cleanliness = models.BooleanField(null=True)
    decor = models.BooleanField(null=True)
    drink = models.BooleanField(null=True)
    entertainment = models.BooleanField(null=True)
    food = models.BooleanField(null=True)
    quality = models.BooleanField(null=True)
    service = models.BooleanField(null=True)
    speed = models.BooleanField(null=True)
    value = models.BooleanField(null=True)

    def get_field_names(cls):
        names = []
        for field in Feedback._meta.fields:
            if field.name != "id" and field.name != 'review':
                names.append(field.name)
        return names

    def get_counts(self):
        """
        Returns the (Total, True, False) counts as tuple
        """
        pos = 0
        neg = 0
        for field in Feedback._meta.fields:
            if field.name != "id" and field.name != 'review':
                if field.value_from_object(self) is True:
                    pos += 1
                elif field.value_from_object(self) is False:
                    neg += 1
        return (pos, neg)

class Scorecard(models.Model):
    """
    Maintains an updated score of each possible place attribute
    """
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    scores = models.JSONField(default=dict)

    def update_record_with_newest_review(self, user):
        """
        Updates the place review record with a user's newest review
        """
        reviews = Review.objects.filter(reviewer = user)
        print(reviews[0])
