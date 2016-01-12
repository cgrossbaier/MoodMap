import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Event

#
class EventMethodTests(TestCase):
    
    user = User(username="test", password="test");

    def test_was_saved_properly(self):
        """
        was_saved_properly() should return True when Event was saved properly.
        """
        event = Event();
        event.user = user;
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        event.eventType = models.CharField(max_length=200)
        event.description = models.CharField(max_length=800)
        event.creation_date = models.DateTimeField('date published')
        event.valid_until = models.DateTimeField('date published')
        event.lng = models.FloatField()
        event.lat = models.FloatField()
        event.time = timezone.now() + datetime.timedelta(days=30)
        self.assertEqual(future_question.was_published_recently(), False)