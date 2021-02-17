from django.test import TestCase
from django.core import mail
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


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Marcel Bittar', cpf='12345678901',
                    email='ma_bittar@yahoo.com', phone='21-98888-2134')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """
        Valid POST should redirect to /inscicao/
        """
        self.assertEqual(302, self.resp.status_code)

    def test_send_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com', 'ma_bittar@yahoo.com']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Marcel Bittar', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('ma_bittar@yahoo.com', email.body)
        self.assertIn('21-98888-2134', email.body)


class SubscribeInvalidPost(TestCase):

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
                    email='ma_bittar@yahoo.com', phone='21-98888-2134')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')

    
