from django.contrib import admin
from django.utils.timezone import now
from eventex.subscriptions.models import Subscriptions


class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'cpf',
                    'created_at', 'subscribed_today', 'paid')
    date_hierarchy = 'created_at'  # seleciona a data de inscrição
    # abre o campo de pesquisa
    search_fields = ('name', 'email', 'phone', 'created_at')
    list_filter = ('paid', 'created_at')

    actions = ['mark_as_paid']

    # filtrando os inscritos hoje
    def subscribed_today(self, obj):
        return obj.created_at == now().date()

    # renomeando a coluna e indicando ícone
    subscribed_today.short_description = 'inscrito hoje?'
    subscribed_today.boolean = True

    def mark_as_paid(self, request, queryset):
        count = queryset.update(paid=True)

        if count == 1:
            msg = '{} inscrição foi marcada como paga.'
        else:
            msg = '{} inscições foram marcadas como pagas.'

        self.message_user(request=request, message=msg.format(count))

    mark_as_paid.short_description = 'Marcar como pago'


admin.site.register(Subscriptions, SubscriptionModelAdmin)
