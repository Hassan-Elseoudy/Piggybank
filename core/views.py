from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from core.models import Currency, Category, Transaction
from core.serializers import CurrencySerializer, CategorySerializer, WriteTransactionSerializer, \
    ReadTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None  # We can set it here


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionModelViewSet(ModelViewSet):
    queryset = Transaction.objects.select_related("currency", "category")
    filter_backends = [filters.SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['description']
    ordering_fields = ['amount', 'date']
    filterset_fields = ["currency__code",]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer

        return WriteTransactionSerializer
