from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Entry


class EntryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.entry = Entry.objects.create(name='Test Entry', description='Test Description')

    def test_get_entries(self):
        response = self.client.get(reverse('entry-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add tests for other CRUD operations (create, retrieve, update, delete)
