from rest_framework import serializers

from carts.models import Cart


class CartSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    product_number = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_name(self, obj: Cart) -> str:
        return obj.product.name

    def get_product_number(self, obj: Cart) -> str:
        return obj.product.product_number

    def get_price(self, obj: Cart) -> int:
        return obj.product.price

    def get_total(self, obj: Cart) -> int:
        return obj.quantity * obj.product.price

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'product',
            'quantity',
            'name',
            'product_number',
            'total',
            'price',
        ]
        read_only_fields = ('user',)


class CartAddSerializer(serializers.Serializer):
    product = serializers.IntegerField(required=True)


