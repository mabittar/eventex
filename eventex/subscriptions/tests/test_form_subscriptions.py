from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionsFormTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have  fields"""
        self.form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_cpf_has_eleven_digits(self):
        # CPF must contains 11 digits
        form = self.make_validated_form(cpf='1234')

        self.assertListEqual(['cpf'], list(form.errors))

        self.assertFormErrorCode(form, 'cpf', 'len')

    def test_cpf_is_digits(self):
        # CPF must only accepts digits
        form = self.make_validated_form(cpf='12345678abc')
        self.assertListEqual(['cpf'], list(form.errors))

        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_is_invalid(self):
        # CPF must only accepts digits
        form = self.make_validated_form(cpf='01234567891')
        self.assertListEqual(['cpf'], list(form.errors))

        self.assertFormErrorCode(form, 'cpf', 'lógica')

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def make_validated_form(self, **kwargs):
        valid = dict(
            name='Marcel Bittar',
            cpf='01234567890',
            email='ma_bittar@yahoo.com.br',
            phone='21-9-8224-7260'
        )
        data = dict(
            valid, **kwargs
        )
        form = SubscriptionForm(data)
        form.is_valid()

        return form
