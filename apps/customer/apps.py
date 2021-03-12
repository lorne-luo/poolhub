from django.apps import AppConfig
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save


class CustomerConfig(AppConfig):
    name = 'apps.customer'

    def ready(self):
        from .models import Customer

        print(11231231231)
        channel_layer = get_channel_layer()
        group_send = async_to_sync(channel_layer.group_send)
        model_label = 'customer.Customer'

        def receiver(sender, instance, **kwargs):
            print('######')
            print(instance)
            payload = {
                'type': 'customer.changed',
                'pk': instance.pk,
                'model': model_label
            }
            group_send(f'django.{model_label}', payload)

        post_save.connect(receiver, sender='customer.Customer', weak=False,
                          dispatch_uid=f'django.{model_label}')
