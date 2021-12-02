from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from core.models import Currency, Category, Transaction
from core.serializers import CurrencySerializer, CategorySerializer, WriteTransactionSerializer, \
    ReadTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionModelViewSet(ModelViewSet):
    queryset = Transaction.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer

        return WriteTransactionSerializer
