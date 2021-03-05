from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscriptions


class SubscriptionsModelTest(TestCase):
	def setUp(self):
		self.obj = Subscriptions(
			name='Marcel Bittar',
			cpf='12345678901',
			email='ma_bittar@yahoo.com.br',
			phone='21-9-8224-7260'
		)
		self.obj.save()

	def test_create(self):
		self.assertTrue(Subscriptions.objects.exists)

	def test_created_at(self):
		"""subscriptions must have an auto create_at attribute"""
		self.assertIsInstance(self.obj.created_at, datetime)

	def test_str(self):
		self.assertEqual('Marcel Bittar', str(self.obj))

class SubscriptionNotFound(TestCase):
	def test_not_found(self):
		resp = self.client.get('/inscricao/0/')
		self.assertEqual(404, resp.status_code)