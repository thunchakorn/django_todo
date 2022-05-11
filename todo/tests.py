from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now

from todo.models import Priority, Todo  # ,Comment, Following, Participant

from datetime import timedelta


class TodoTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser1", password="12345")
        self.priority_test = Priority(level="Low")

    def test_is_public_defualt(self):
        todo1 = Todo(
            name="test",
            detail="test-detail",
            owner=self.user1,
            due=now() + timedelta(days=5),
            priority=self.priority_test,
        )
        self.assertFalse(todo1.is_public)
