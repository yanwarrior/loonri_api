from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer
from utils.helpers import auto_number


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    search_fields = ['name', 'product_number']
    prefix = 'BRG'

    @action(detail=False, methods=['POST'])
    def get_number(self, request):
        return Response({
            'number': auto_number(Product, self.prefix)
        })


