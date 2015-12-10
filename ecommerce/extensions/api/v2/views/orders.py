"""HTTP endpoints for interacting with orders."""
import logging

from oscar.core.loading import get_model, get_class
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response

from ecommerce.extensions.api import serializers
from ecommerce.extensions.api.constants import APIConstants as AC
from ecommerce.extensions.api.permissions import IsStaffOrOwner
from ecommerce.extensions.api.throttles import ServiceUserThrottle

logger = logging.getLogger(__name__)

Order = get_model('order', 'Order')


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = AC.KEYS.ORDER_NUMBER
    # TODO Make sure non-staff users cannot fulfill orders
    permission_classes = (IsAuthenticated, IsStaffOrOwner, DjangoModelPermissions,)
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    throttle_classes = (ServiceUserThrottle,)

    def filter_queryset(self, queryset):
        queryset = super(OrderViewSet, self).filter_queryset(queryset)
        user = self.request.user

        # Non-staff users should only see their own orders
        if not user.is_staff:
            queryset = queryset.filter(user=user)

        return queryset

    @detail_route(methods=['post'])
    def fulfill(self, request, number=None):
        """ Fulfill order """
        order = self.get_object()

        if not order.is_fulfillable:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        logger.info('Attempting fulfillment of order [%s]...', order.number)
        post_checkout = get_class('checkout.signals', 'post_checkout')
        post_checkout.send(sender=post_checkout, order=order)

        if order.is_fulfillable:
            logger.warning('Fulfillment of order [%s] failed!', order.number)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(order)
        return Response(serializer.data)
