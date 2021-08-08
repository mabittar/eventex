from django import forms
from django.core.exceptions import ValidationError
from validate_docbr import CPF

def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas dígitos.', code='digits')

    if len(value) != 11:
        raise ValidationError('CPF deve conter 11 números.', code='len')

    cpf = CPF()
    if not cpf.validate(str(value)):
        raise ValidationError('CPF inválido', code='lógica')

class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF', validators=[validate_cpf])
    email = forms.EmailField(label='E-mail', required=False)
    phone = forms.CharField(label='Telefone: ', required=False)

    def clean_name(self):
        name = self.cleaned_data['name']
        words = [w.capitalize() for w in name.split()]
        return ' '.join(words)

    def clean(self):
        if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
            raise ValidationError('Informe seu e-mail ou telefone.', code='phone_or_email')
