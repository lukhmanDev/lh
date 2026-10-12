from typing import Any

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from contact.models import ContactMessage



class ContactMessageApiTests(APITestCase):
    client: Any

    def test_creates_contact_message(self):
        response = self.client.post(
            reverse('contact-message-create'),
            {
                'name': 'Alex Morgan',
                'email': 'alex@example.com',
                'subject': 'Project inquiry',
                'message': 'Tell me about your project.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(response.data['email'], 'alex@example.com')

    def test_requires_message(self):
        response = self.client.post(
            reverse('contact-message-create'),
            {'name': 'Alex Morgan', 'email': 'alex@example.com'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)

    def test_get_messages_list(self):
        ContactMessage.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            subject='First Message',
            message='Hello world',
        )
        ContactMessage.objects.create(
            name='John Smith',
            email='john@example.com',
            subject='Second Message',
            message='Another message',
        )

        response = self.client.get(reverse('contact-message-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'John Smith')

    def test_get_single_message_by_id(self):
        msg = ContactMessage.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            subject='Test Subject',
            message='Test Content',
        )

        url = reverse('contact-message-detail', kwargs={'pk': msg.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], msg.id)
        self.assertEqual(response.data['name'], 'Jane Doe')
        self.assertEqual(response.data['email'], 'jane@example.com')
        self.assertEqual(response.data['message'], 'Test Content')

    def test_get_single_message_not_found(self):
        url = reverse('contact-message-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

