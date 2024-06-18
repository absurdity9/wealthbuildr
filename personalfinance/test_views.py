from django.test import TestCase, Client
from personalfinance.views import create_user_profile
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from personalfinance.models import Userprofile
import json

class TestCreateUserProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_user_profile_valid_request(self):
        # Create a new user profile with valid data
        userprofile_data = {'user_id': self.user.id, 'age': '30', 'job': 'Software Engineer'}
        response = self.client.post(reverse('create_user_profile'), userprofile_data)
        self.assertEqual(response.status_code, 200)

        # Check the response data
        response_data = json.loads(response.content)
        self.assertEqual(response_data['user_id'], self.user.id)
        self.assertEqual(response_data['age'], '30')
        self.assertEqual(response_data['job'], 'Software Engineer')

    def test_create_user_profile_invalid_user_id(self):
        userprofile_data = {'user_id': 123456, 'age': '30', 'job': 'Software Engineer'}
        response = self.client.post(reverse('create_user_profile'), userprofile_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'User not found'})

    def test_create_user_profile_missing_data(self):
        userprofile_data = {'user_id': self.user.id, 'age': '30'}
        response = self.client.post(reverse('create_user_profile'), userprofile_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Missing profile data'})

    def test_create_user_profile_non_post_request(self):
        response = self.client.get(reverse('create_user_profile'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Invalid request method'})

class TestCreateFModel(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_fmodel_valid_request(self):
        # Create a new FModel with valid data
        fmodel_data = {'user_id': self.user.id, 'fmodel_name': 'Test FModel'}
        response = self.client.post(reverse('create_fmodel'), fmodel_data)
        self.assertEqual(response.status_code, 201)

        # Check the response data
        response_data = json.loads(response.content)
        self.assertEqual(response_data['user'], self.user.id)
        self.assertEqual(response_data['fmodel_name'], 'Test FModel')

    def test_create_fmodel_non_existent_user(self):
        fmodel_data = {'user_id': 123456, 'fmodel_name': 'Test FModel', 'created': '2023-06-18'}
        response = self.client.post(reverse('create_fmodel'), fmodel_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'User not found'})

    def test_create_fmodel_missing_data(self):
        fmodel_data = {'user_id': self.user.id, 'fmodel_name': 'Test FModel'}
        response = self.client.post(reverse('create_fmodel'), fmodel_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Missing required fields'})

    def test_create_fmodel_non_post_request(self):
        response = self.client.get(reverse('create_fmodel'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Invalid request method'})