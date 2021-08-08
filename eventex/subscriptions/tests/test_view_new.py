from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscriptions


class SubscriptionsNewGet(TestCase):

    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))

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


class SubscriptionsNewPost(TestCase):
    def setUp(self):
        data = dict(name='Marcel Bittar', cpf='01234567890',
                    email='ma_bittar@yahoo.com.br', phone='21-98888-2134')
        self.resp = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        """
        Valid POST should redirect to /inscricao/86a04bab-a8be-4d49-8c0e-11ae0c11daf9/
        """
        # self.assertEqual(302, self.resp.status_code)
        subscription = self.resp.context['subscription'].hashid
        self.assertRedirects(self.resp, r('subscriptions:detail', subscription))

    def test_send_email(self):
        """
        Should send 1 email
        """
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscriptions(self):
        self.assertTrue(Subscriptions.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):

    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})

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

    def test_dont_save_subscription(self):
        self.assertFalse(Subscriptions.objects.exists())

# teste removido após redirecionamento para inscricao/1/
# @unittest.skip('To be removed')
# class SubscribeSuccessMessage(TestCase):
#     def test_message(self):
#         data = dict(name='Marcel Bittar', cpf='12345678901',
#                     email='ma_bittar@yahoo.com.br', phone='21-98888-2134')
#
#         response = self.client.post('/inscricao/', data, follow=True)
#         self.assertContains(response, 'Inscrição realizada com sucesso!')

class TemplateRegressionTest(TestCase):
    def test_template_has_non_field_erros(self):
        invalid_data = dict(name='Marcel Bittar', cpf='01234567890')
        response = self.client.post(r('subscriptions:new'), invalid_data)

        self.assertContains(response, '<ul class="errorlist nonfield">')
