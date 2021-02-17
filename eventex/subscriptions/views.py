from django.shortcuts import render
from eventex.subscriptions.forms import SubscriptionForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            # context = dict(name='Marcel Bittar', cpf='12345678901',
            #                email='ma_bittar@yahoo.com', phone='21-98888-2134')
            body = render_to_string(
                'subscriptions/subscription_email.txt', form.cleaned_data)

            mail.send_mail('Confirmação de Inscrição',
                           body,
                           'contato@eventex.com',
                           ['contato@eventex.com', form.cleaned_data['email']]
                           )

            messages.success(request, 'Inscrição realizada com sucesso!')

            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html', {'form': form})
    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)
