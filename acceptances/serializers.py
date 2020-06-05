from rest_framework import serializers

from acceptances.models import Acceptance, Item


class AcceptanceSerializer(serializers.ModelSerializer):
    payment_status = serializers.SerializerMethodField()
    attr_color_payment_status = serializers.SerializerMethodField()
    attr_status = serializers.SerializerMethodField()

    def get_attr_status(self, obj: Acceptance) -> str:
        if obj.status == Acceptance.STATUS_TAKED:
            return 'Sudah Diambil'
        elif obj.status == Acceptance.STATUS_COMPLETED:
            return 'Cucian Selesai'
        else:
            return 'Sedang Dicuci'

    def get_payment_status(self, obj: Acceptance) -> str:
        total = obj.total
        dp = obj.down_payment
        residual = obj.residual

        if dp == 0:
            return 'Belum Lunas'
        elif residual < total and residual > 0:
            return 'Piutang'
        else:
            return 'Lunas'

    def get_attr_color_payment_status(self, obj: Acceptance) -> str:
        total = obj.total
        dp = obj.down_payment
        residual = obj.residual

        if dp == 0:
            return 'danger'
        elif residual < total and residual > 0:
            return 'warning'
        else:
            return 'success'

    class Meta:
        model = Acceptance
        fields = [
            'id',
            'acceptance_number',
            'acceptance_date',
            'user',
            'customer_name',
            'customer_address',
            'customer_phone',
            'total',
            'down_payment',
            'residual',
            'status',
            'payment_status',
            'attr_color_payment_status',
            'attr_status',
        ]
        read_only_fields = ['user',]


class ItemSerializer(serializers.ModelSerializer):
    acceptance_number = serializers.SerializerMethodField()

    def get_acceptance_number(self, obj: Item) -> str:
        return obj.acceptance.acceptance_number

    product_number = serializers.SerializerMethodField()

    def get_product_number(self, obj: Item) -> str:
        return obj.product.product_number

    product_name = serializers.SerializerMethodField()

    def get_product_name(self, obj: Item) -> str:
        return obj.product.name

    class Meta:
        model = Item
        fields = [
            'id',
            'acceptance',
            'acceptance_number',
            'product',
            'product_number',
            'product_name',
            'quantity',
            'unit',
            'price',
            'sub_total',
        ]