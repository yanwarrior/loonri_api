from rest_framework import serializers

from accounting.models import Profoss


class ProfossSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profoss
        fields = [
            'id',
            'purpose',
            'date',
            'cost_in',
            'cost_out',
            'user',
            'acceptance',
        ]
        read_only_fields = ['user',]