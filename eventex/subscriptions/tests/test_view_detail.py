from django.test import TestCase
from eventex.subscriptions.models import Subscriptions


class SubscriptionDetailGet(TestCase):
	def setUp(self):
		self.obj = Subscriptions.objects.create(
			name='Marcel Bittar',
			cpf='12345678901',
			email='ma_bittar@yahoo.com.br',
			phone='21-98888-2134')
		self.resp = self.client.get('/inscricao/{}/'.format(self.obj.pk))

	def test_get(self):
		self.assertEqual(200, self.resp.status_code)

	def test_template(self):
		self.assertTemplateUsed(self.resp, 'subscriptions/subscription_detail.html')

	def test_context(self):
		subscription = self.resp.context['subscription']
		self.assertIsInstance(subscription, Subscriptions)

	def test_html(self):
		contents = (self.obj.name, self.obj.cpf, self.obj.email, self.obj.phone)

		with self.subTest():
			for expected in contents:
				self.assertContains(self.resp, expected)
