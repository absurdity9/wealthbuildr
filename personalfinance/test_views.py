from django.test import TestCase, Client
from rest_framework.reverse import reverse
from django.contrib.auth.models import User 
from personalfinance.models import Userprofile, FModel, Income, Expense, Asset, ProfilePage
import json

class TestCreateUserProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_user_profile_valid_request(self):
        userprofile_data = {'user_id': self.user.id, 'age': '30', 'job': 'Software Engineer'}
        response = self.client.post(reverse('create_user_profile'), userprofile_data)
        self.assertEqual(response.status_code, 200)

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
        fmodel_data = {'user_id': self.user.id, 'fmodel_name': 'Test FModel'}
        response = self.client.post(reverse('create_fmodel'), fmodel_data)
        self.assertEqual(response.status_code, 201)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['user'], self.user.id)
        self.assertEqual(response_data['fmodel_name'], 'Test FModel')

    def test_create_fmodel_non_existent_user(self):
        fmodel_data = {'user_id': 123456, 'fmodel_name': 'Test FModel', 'created': '2023-06-18'}
        response = self.client.post(reverse('create_fmodel'), fmodel_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'User not found'})

    def test_create_fmodel_missing_data(self):
        fmodel_data = {'user_id': self.user.id}
        response = self.client.post(reverse('create_fmodel'), fmodel_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Missing required fields'})

    def test_create_fmodel_non_post_request(self):
        response = self.client.get(reverse('create_fmodel'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Invalid request method'})

    def test_create_fmodel_duplicate_name(self):
        initial_fmodel = FModel.objects.create(user=self.user, fmodel_name='Test FModel')

        fmodel_data = {'user_id': self.user.id, 'fmodel_name': 'Test FModel'}
        response = self.client.post(reverse('create_fmodel'), fmodel_data)

        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.content)
        self.assertEqual(response_data, {'error': 'FModel with this name already exists for this user'})

class TestCreateIncome(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.fmodel = FModel.objects.create(user=self.user, fmodel_name='Test FModel')

    def test_create_income_valid_request(self):
        income_data = {'user_id': self.user.id, 'fmodel_name': 'Test FModel', 'income_name': 'Test Income', 'value': '1000.00'}
        response = self.client.post(reverse('create_income'), income_data)
        self.assertEqual(response.status_code, 201)

        response_data = json.loads(response.content)
        fmodel = FModel.objects.get(user=self.user, fmodel_name=income_data['fmodel_name'])
        self.assertEqual(response_data['fmodel_id'], fmodel.id)
        self.assertEqual(response_data['income_name'], 'Test Income')
        self.assertEqual(response_data['value'], '1000.00')

    def test_create_income_non_existent_user_or_fmodel(self):
        income_data = {'user_id': 123456, 'fmodel_id': 654321, 'income_name': 'Test Income', 'value': '1000.00'}
        response = self.client.post(reverse('create_income'), income_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Missing required fields'})

    def test_create_income_missing_data(self):
        income_data = {'user_id': self.user.id, 'fmodel_name': 'Test FModel', 'income_name': 'Test Income'}
        response = self.client.post(reverse('create_income'), income_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Missing required fields'})

    def test_create_income_non_post_request(self):
        response = self.client.get(reverse('create_income'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Invalid request method'})

class TestCreateExpense(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.fmodel = FModel.objects.create(user=self.user, fmodel_name='Test FModel')

    def test_create_expense_valid_request(self):
        expense_data = {
            'user_id': self.user.id,
            'fmodel_name': 'Test FModel',
            'expenses': [
                {'expense_name': 'Rent', 'value': '1000.00'},
                {'expense_name': 'Groceries', 'value': '200.00'}
            ]
        }
        response = self.client.post(reverse('create_expense'), json.dumps(expense_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['expenses']), 2)

        for expense in response_data['expenses']:
            self.assertEqual(expense['fmodel_id'], 1)
            self.assertIn(expense['expense_name'], ['Rent', 'Groceries'])
            self.assertIn(expense['value'], ['1000.00', '200.00'])

    def test_create_expense_missing_required_fields(self):
        expense_data = {
            'user_id': self.user.id,
            'expenses': [
                {'expense_name': 'Rent', 'value': '1000.00'},
                {'expense_name': 'Groceries'}
            ]
        }
        response = self.client.post(reverse('create_expense'), json.dumps(expense_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Missing required fields'})

    def test_create_expense_user_or_fmodel_not_found(self):
        expense_data = {
            'user_id': 999,
            'fmodel_name': 'Non-existent FModel',
            'expenses': [
                {'expense_name': 'Rent', 'value': '1000.00'},
                {'expense_name': 'Groceries', 'value': '200.00'}
            ]
        }
        response = self.client.post(reverse('create_expense'), json.dumps(expense_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'User or FModel not found'})

    def test_create_expense_invalid_request_method(self):
        response = self.client.get(reverse('create_expense'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Invalid request method'})

class TestCreateAsset(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.fmodel = FModel.objects.create(user=self.user, fmodel_name='Test FModel')

    def test_create_asset_valid_request(self):
        asset_data = {'user_id': self.user.id, 'fmodel_name': 'Test FModel', 'asset_name': 'Test Asset', 'yield_rate': '5.0', 'principle_amount': '1000.00'}
        response = self.client.post(reverse('create_asset'), asset_data)
        self.assertEqual(response.status_code, 201)

        response_data = json.loads(response.content)
        fmodel = FModel.objects.get(user=self.user, fmodel_name=asset_data['fmodel_name'])
        self.assertEqual(response_data['fmodel_id'], fmodel.id)
        self.assertEqual(response_data['asset_name'], 'Test Asset')
        self.assertEqual(response_data['yield_rate'], '5.0')
        self.assertEqual(response_data['principle_amount'], '1000.00')

    def test_create_asset_non_existent_user_or_fmodel(self):
        asset_data = {'user_id': 123456, 'fmodel_name': 'NonExistent FModel', 'asset_name': 'Test Asset', 'yield_rate': '5.0', 'principle_amount': '1000.00'}
        response = self.client.post(reverse('create_asset'), asset_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'User or FModel not found'})

    def test_create_asset_missing_data(self):
        asset_data = {'user_id': self.user.id, 'fmodel_name': 'Test FModel', 'asset_name': 'Test Asset', 'yield_rate': '5.0'}
        response = self.client.post(reverse('create_asset'), asset_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Missing required fields'})

    def test_create_asset_non_post_request(self):
        response = self.client.get(reverse('create_asset'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Invalid request method'})

class TestCreateProfilePage(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.fmodel = FModel.objects.create(user=self.user, fmodel_name='Test FModel')

    def test_create_profile_page_valid_request(self):
        profile_page_data = {'user_id': self.user.id, 'fmodel_name': 'Test FModel', 'page_name': 'Test Page'}
        response = self.client.post(reverse('create_profile_page'), profile_page_data)
        self.assertEqual(response.status_code, 201)

        response_data = json.loads(response.content)
        fmodel = FModel.objects.get(user=self.user, fmodel_name=profile_page_data['fmodel_name'])
        self.assertEqual(response_data['user_id'], self.user.id)
        self.assertEqual(response_data['fmodel_id'], fmodel.id)
        self.assertEqual(response_data['page_name'], 'Test Page')

    def test_create_profile_page_non_existent_user_or_fmodel(self):
        profile_page_data = {'user_id': 123456, 'fmodel_name': 'NonExistent FModel', 'page_name': 'Test Page'}
        response = self.client.post(reverse('create_profile_page'), profile_page_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'User or FModel not found'})

    def test_create_profile_page_missing_data(self):
        profile_page_data = {'user_id': self.user.id, 'fmodel_name': 'Test FModel'}
        response = self.client.post(reverse('create_profile_page'), profile_page_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Missing required fields'})

    def test_create_profile_page_non_post_request(self):
        response = self.client.get(reverse('create_profile_page'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Invalid request method'})
