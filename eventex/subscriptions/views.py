from django.conf import settings
from django.core import mail
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscriptions


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = Subscriptions.objects.create(**form.cleaned_data)

    # caso o formulário não seja válido e retorna na linha anterior, caso contrário segue o fluxo
    # send email
    _send_email('Confirmação de Inscrição',
                settings.DEFAULT_FROM_EMAIL,
                subscription.email,
                'subscriptions/subscription_email.txt',
                {'subscription': subscription})

    # success feedback - ALTERADO para retornar diretamente para inscricao/1/
    # messages.success(request, 'Inscrição realizada com sucesso!')

    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.hashid))


def new(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def detail(request, hashid):
    try:
        subscription = Subscriptions.objects.get(hashid=hashid)
    except Subscriptions.DoesNotExist:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html',
                  {'subscription': subscription})


def _send_email(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
