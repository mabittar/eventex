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

    def test_name_must_be_capitalized(self):
        '''name must be capitalized marcel bittar -> Marcel Bittar'''
        form = self.make_validated_form(name='MARCEL bittar')
        self.assertEqual('Marcel Bittar', form.cleaned_data['name'])

    def test_email_is_optional(self):
        '''email is optional'''
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        '''phone is optional'''
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_phone_or_email_must_be_informed(self):
        '''email or phone is optional but at last one must be informed'''
        form = self.make_validated_form(phone='', email='')
        self.assertListEqual(['__all__'], list(form.errors))

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
