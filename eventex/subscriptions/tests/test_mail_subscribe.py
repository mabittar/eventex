from django.test import TestCase
from django.core import mail
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Marcel Bittar', cpf='12345678901',
                    email='ma_bittar@yahoo.com.br', phone='21-98888-2134')
        self.resp = self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de Inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'ma_bittar@yahoo.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['ma_bittar@yahoo.com.br', 'ma_bittar@yahoo.com.br']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Marcel Bittar',
                    '12345678901',
                    'ma_bittar@yahoo.com.br',
                    '21-98888-2134']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

        # Refatorado pelo iterador acima
        # self.assertIn('Marcel Bittar', self.email.body)
        # self.assertIn('12345678901', self.email.body)
        # self.assertIn('ma_bittar@yahoo.com.br', self.email.body)
        # self.assertIn('21-98888-2134', self.email.body)
