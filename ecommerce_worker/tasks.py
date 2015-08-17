from __future__ import absolute_import
import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def process_order(order_id):
    logger.info('Order arrived: order_id=%s', order_id)



