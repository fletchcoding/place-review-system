import datetime

from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

class PLACE_ATTRIBUTES():
    attr_list = (
        ('AT', 'Atmosphere'),
        ('CL', 'Cleanliness'),
        ('DE', 'Decor'),
        ('DR', 'Drink'),
        ('EN', 'Entertainment'),
        ('FO', 'Food'),
        ('QU', 'Quality'),
        ('SE', 'Service'),
        ('SP', 'Speed'),
        ('VA', 'Value'),
    )

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
    review_date = models.DateTimeField('Date review published', null=True, blank=True)
    visit_date = models.DateTimeField('Visit date and time', default=timezone.now())

    positive_feedback = ArrayField(
        models.CharField(choices=PLACE_ATTRIBUTES.attr_list, max_length=4),
        blank=True,
        null=True,
        unique=True
    )
    negative_feedback = ArrayField(
        models.CharField(choices=PLACE_ATTRIBUTES.attr_list, max_length=4),
        blank=True,
        null=True,
        unique=True
    )

    def __str__(self):
        return str(self.place) + ', by ' + str(self.visit_date)

    def check_feedback_count(self):
        """
        Returns the total number of rated attrbutes
        """
        return len(self.positive_feedback) + len(self.negative_feedback)

    def check_unique(self):
        """
        Returns true if positive_feedback and negative_feedback contain
         unique items
        """
        return True if (len(set(self.positive_feedback).intersection(self.negative_feedback)) == 0) else False

    def save(self, *args, **kwargs):
        """
        Override save function to check unique model constraints
        """
        if self.check_unique()==False:
            raise ValidationError("Cannot rate an attribute BOTH negatively and positively.")

        if self.check_feedback_count()<3:
            raise ValidationError("Minimum of 3 attribute feedbacks required.")

        super().save(*args, **kwargs)


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
