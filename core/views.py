# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from core.models import Currency, Category, Transaction
from core.reports import transaction_report
from core.serializers import CurrencySerializer, CategorySerializer, WriteTransactionSerializer, \
    ReadTransactionSerializer, ReportEntrySerializer, ReportParamsSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None  # We can set it here


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['description']
    ordering_fields = ['amount', 'date']
    filterset_fields = ["currency__code", ]

    def get_queryset(self):
        return Transaction.objects.select_related("currency", "category", "user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer

        return WriteTransactionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionReportAPIView(APIView):

    def get(self, request):
        params_serializer = ReportParamsSerializer(data=request.GET, context={"request": request})
        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.save()

        data = transaction_report(params)
        serializer = ReportEntrySerializer(instance=data, many=True)
        return Response(data=serializer.data)
