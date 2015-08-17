from django.db.models.signals import post_save
from django.dispatch import receiver

from ecommerce_worker.tasks import process_order

from ecommerce.extensions.order.models import Order

@receiver(post_save, sender=Order)
def order_post_save(sender, **kwargs):
    # emit message via celery
    process_order.apply_async(kwargs={'order_id': kwargs['instance'].id})
