from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):

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
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """form must contain CSRF Token"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """ Form must have  fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(
            ['name', 'cpf', 'email', 'phone'], list(form.fields))
