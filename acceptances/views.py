from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from acceptances.models import Acceptance, Item
from acceptances.serializers import AcceptanceSerializer, ItemSerializer
from carts.models import Cart
from utils.helpers import auto_number


class AcceptanceViewSet(viewsets.ModelViewSet):
    queryset = Acceptance.objects.all()
    serializer_class = AcceptanceSerializer
    search_fields = ['acceptance_number', 'customer_name', 'customer_phone']
    prefix = 'ORD'
    filter_fields = ('status',)

    @action(detail=False, methods=['POST'])
    def get_number(self, request):
        return Response({
            'number': auto_number(Acceptance, self.prefix)
        })

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['POST'])
    def cart_to_item(self, request, pk=None):
        acceptance = self.get_object()
        carts = Cart.objects.all()
        total = 0

        items = []
        for cart in carts:
            sub_total = cart.product.price * cart.quantity
            total += sub_total
            item = Item(
                acceptance=acceptance,
                product=cart.product,
                quantity=cart.quantity,
                unit=cart.product.unit,
                price=cart.product.price,
                sub_total=sub_total
            )
            items.append(item)

        Item.objects.bulk_create(items)
        acceptance.total = total
        acceptance.residual = total - acceptance.down_payment
        acceptance.save()

        carts.delete()
        return Response(self.serializer_class(acceptance).data, status=200)

    @action(detail=True, methods=['POST'])
    def completed(self, request, pk=None):
        acceptance = self.get_object()
        acceptance.status = Acceptance.STATUS_COMPLETED
        acceptance.save()

        return Response(self.serializer_class(acceptance).data, status=200)

    @action(detail=True, methods=['POST'])
    def taked(self, request, pk=None):
        acceptance = self.get_object()
        acceptance.status = Acceptance.STATUS_TAKED
        acceptance.down_payment = acceptance.total
        acceptance.residual = 0
        acceptance.save()

        return Response(self.serializer_class(acceptance).data, status=200)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    search_fields = [
        'acceptance__acceptance_number',
        'product__name',
    ]
    filter_fields = ('acceptance', )
