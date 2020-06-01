from django.db.models import Count, Sum, IntegerField, F, PositiveIntegerField
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from carts.models import Cart
from carts.serializers import CartSerializer, CartAddSerializer
from products.models import Product


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    search_fields = ['product__name', 'product__product_number']
    filterset_fields = ['product',]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['POST'])
    def add(self, request):
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, pk=serializer.data.get('product'))
        # get or create
        cart, created = Cart.objects.get_or_create(
            product=product,
            user=self.request.user
        )

        cart.quantity += 1
        cart.save()

        return Response(self.serializer_class(cart).data, status=201)

    @action(detail=False, methods=['GET'])
    def total(self, request):
        cart = Cart.objects.filter(
            user=request.user
        ).aggregate(
            item=Count('product'),
            total=Sum(F('product__price') * F('quantity'))
        )

        return Response(cart, status=200)
