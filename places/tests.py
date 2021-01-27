from django.utils import timezone
from django.test import TestCase
from .models import Place, Review, Feedback, Scorecard
from django.contrib.auth.models import User

def create_fake_place(name):
    """
    Creates a dummy place object with input name
    """
    place = Place(name=name, street_address="123 Fake St", suburb="Alsofake",
        state="FAK", postcode=1234)
    return place

def create_fake_user(name):
    """
    Creats a fake user object with input name
    """
    user = User.objects.create_user(username=name, password='12345')
    return user

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
        attrs = ['atmosphere',
            'cleanliness',
            'decor',
            'drink',
            'entertainment',
            'food',
            'quality',
            'service',
            'speed',
            'value'
        ]
        self.assertEqual(feedback.get_field_names(), attrs)

    def test_get_fieldnames_unique(self):
        """
        get_fieldnames() returns a unique list
        """
        feedback = Feedback()
        self.assertEqual(len(set(feedback.get_field_names())),
            len(feedback.get_field_names()))
