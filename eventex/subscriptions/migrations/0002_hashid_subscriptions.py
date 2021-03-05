from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
	dependencies = [('subscriptions', '0001_initial'),]

	operations = [
		migrations.AddField(
			model_name='Subscriptions',
			name='hashid',
			field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='hashID')

		),
	]
