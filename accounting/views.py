from django.shortcuts import render
from rest_framework import viewsets

from accounting.models import Profoss
from accounting.serializers import ProfossSerializer


class ProfossViewSet(viewsets.ModelViewSet):
    serializer_class = ProfossSerializer
    queryset = Profoss.objects.all()
    search_fields = ['acceptance__acceptance_number', 'user__username', 'purpose',]
    filter_fields = ('user', 'acceptance', 'cost_in', 'cost_out',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


