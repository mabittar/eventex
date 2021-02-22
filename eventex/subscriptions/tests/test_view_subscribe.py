from django.test import TestCase
from django.core import mail
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeGet(TestCase):

    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """
        Get /inscricao/ must return code 200
        """
        # response = self.client.get('/inscricao/')
        # self.assertEqual(200, response.status_code)
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must uses subscriptions/subscription_form.html
        """
        # response = self.client.get('/inscricao/')
        # self.assertTemplateUsed(
        #     response, 'subscriptions/subscription_form.html')
        self.assertTemplateUsed(
            self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

        # substituído pela iteração anterior
        # self.assertContains(self.resp, '<form')
        # self.assertContains(self.resp, '<input', 6)
        # self.assertContains(self.resp, 'type="text"', 3)
        # self.assertContains(self.resp, 'type="email"')
        # self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """form must contain CSRF Token"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Marcel Bittar', cpf='12345678901',
                    email='ma_bittar@yahoo.com.br', phone='21-98888-2134')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """
        Valid POST should redirect to /inscicao/
        """
        self.assertEqual(302, self.resp.status_code)

    def test_send_email(self):
        """
        Should send 1 email
        """
        self.assertEqual(1, len(mail.outbox))


class SubscribePostInvalid(TestCase):

    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """ Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(
            self.resp, 'subscriptions/subscription_form.html')

    def test_has_from(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Marcel Bittar', cpf='12345678901',
                    email='ma_bittar@yahoo.com.br', phone='21-98888-2134')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
