import datetime
from math import floor

from django.db import models
from django.db.models import Q
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

    def __str__(self):
        """
        Prints the rated attributes.
        """
        pos = ''
        neg = ''
        for field in self.get_field_names():
            if getattr(self, field) == True:
                pos += field + ','
            elif getattr(self, field) == False:
                neg += field + ','
        return 'pos[' + pos + '], neg[' + neg + ']'

    def get_feedback(self, value):
        """
        Returns feedbacks matching value(True/ False)
        """
        ret = []
        for field in self.get_field_names():
            if getattr(self, field) == value:
                ret.append(field)
        return ret


    def get_field_names(cls):
        """
        Helper function to return names of rated attributes
        """
        names = []
        for field in Feedback._meta.fields:
            if field.name != "id" and field.name != 'review':
                names.append(field.name)
        return names

    def get_counts(self):
        """
        Returns the (True, False) counts as tuple
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

    def count_scores(self):
        """
        Counts the scores for all most-current reviews
         Scores must indicate:
         1 - Percentage of attributes (Pos v Neg)
         2 - Percentage of reviews (Attr v Feedbacks)
        """
        counts = {}
        totals = {}
        attributes = {}
        feedbacks = {}

        # Get reviewers of this place
        p = Q(place=self.place)
        users = Review.objects.filter(p).distinct('reviewer').values('reviewer')
        review_count = users.count()
        # Loops over users and gets most recent review
        for u in users:
            # Filter reivews by place per user, taking only latest feedback
            f = Review.objects.filter(p, reviewer=u['reviewer']
                ).latest('visit_date').feedback
            # Loop over positive rated attributes
            for attr in f.get_feedback(True):
                if attr in counts:
                    counts[attr] += 1
                    totals[attr] += 1
                else:
                    counts[attr] = 1
                    totals[attr] = 1
            # Loop over negatively rated attributes
            for attr in f.get_feedback(False):
                if attr in counts:
                    counts[attr] -= 1
                    totals[attr] += 1
                else:
                    counts[attr] = -1
                    totals[attr] = 1

        # Calculate attribute percentages
        outputs = {}
        for attr in counts:
            outputs[attr] = (floor(counts[attr] / totals[attr] * 100),
                floor(totals[attr] / review_count * 100))

        self.scores = outputs
        self.save()
