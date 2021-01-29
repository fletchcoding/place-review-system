from django.utils import timezone
from django.test import TestCase
from .models import Place, Review, Feedback, Scorecard
from django.contrib.auth.models import User

def create_fake_place(name):
    """
    Creates a dummy place object with input name
    """
    Place.objects.create(name=name, street_address="123 Fake St", suburb="Alsofake",
        state="FAK", postcode=1234)

def create_fake_user(name):
    """
    Creates a fake user object with input name
    """
    User.objects.create_user(username=name, password='12345')

def get_attrs():
    return ['atmosphere',
        'cleanliness',
        'decor',
        'drink',
        'entertainment',
        'food',
        'quality',
        'service',
        'speed',
        'value']

class FeedbackModelTests(TestCase):

    def test_get_feedback_no_nulls(self):
        """
        get_feedback() returns empty list if nothing rated
        """
        feedback = Feedback()
        self.assertEqual(feedback.get_feedback(True),[])
        self.assertEqual(feedback.get_feedback(False),[])

    def test_get_feedback_true(self):
        """
        get_feedback() return true attributes only
        """
        feedback = Feedback(atmosphere=True, cleanliness=False)
        self.assertEqual(feedback.get_feedback(True),['atmosphere'])
        self.assertIs('atmosphere' in feedback.get_feedback(False), False)

    def test_get_feedback_false(self):
        """
        get_feedback() returns false attribites only
        """
        feedback = Feedback(atmosphere=True, cleanliness=False)
        self.assertEqual(feedback.get_feedback(False),['cleanliness'])
        self.assertIs('cleanliness' in feedback.get_feedback(True), False)

    def test_get_fieldnames(self):
        """
        get_fieldnames() does not return id or review fields
        """
        feedback = Feedback()
        self.assertIs('id' in feedback.get_field_names(), False)
        self.assertIs('review' in feedback.get_field_names(), False)

    def test_get_fieldnames_all(self):
        """
        get_fieldnames() returns all rateable fields
        """
        feedback = Feedback()
        attrs = get_attrs()
        self.assertEqual(feedback.get_field_names(), attrs)

    def test_get_fieldnames_unique(self):
        """
        get_fieldnames() returns a unique list of attributes
        """
        feedback = Feedback()
        self.assertEqual(len(set(feedback.get_field_names())),
            len(feedback.get_field_names()))

    def test_get_counts_none(self):
        """
        get_counts() returns zero value tuple when no feedback
        """
        feedback = Feedback()
        self.assertEqual(feedback.get_counts(), (0,0))

    def test_get_counts_true(self):
        """
        get_counts() returns correct count of true feedbacks
        """
        feedback = Feedback()
        attrs = get_attrs()
        for attr in attrs:
            setattr(feedback, attr, True)
        self.assertEqual(feedback.get_counts(), (len(attrs),0))

    def test_get_counts_false(self):
        """
        get_counts() returns correct count of false feedbacks
        """
        feedback = Feedback()
        attrs = get_attrs()
        for attr in attrs:
            setattr(feedback, attr, False)
        self.assertEqual(feedback.get_counts(), (0,len(attrs)))

    def test_get_counts_mix(self):
        """
        get_counts() doesn't mix true and false counts
        """
        feedback = Feedback()
        attrs = get_attrs()
        flip = False
        for attr in attrs:
            if flip:
                setattr(feedback, attr, False)
                flip = False
            else:
                setattr(feedback, attr, True)
                flip = True
        self.assertEqual(feedback.get_counts()[0] + feedback.get_counts()[1], len(attrs))
