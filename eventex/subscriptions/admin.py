from django.contrib import admin
from django.utils.timezone import now
from eventex.subscriptions.models import Subscriptions


class SubscriptionModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'phone', 'cpf', 'created_at', 'subscribed_today')
	date_hierarchy = 'created_at'  # seleciona a data de inscrição
	search_fields = ('name', 'email', 'phone', 'created_at')  # abre o campo de pesquisa
	list_filter = ('created_at',)

	# filtrando os inscritos hoje
	def subscribed_today(self, obj):
		return obj.created_at == now().date()

	# renomeando a coluna e indicando ícone
	subscribed_today.short_description = 'inscrito hoje?'
	subscribed_today.boolean = True


admin.site.register(Subscriptions, SubscriptionModelAdmin)