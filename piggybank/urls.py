from django.contrib import admin
from django.urls import path

from core import views

from rest_framework import routers

from core.views import CategoryModelViewSet

router = routers.SimpleRouter()
router.register(r'categories', CategoryModelViewSet, basename="category")

urlpatterns = [
    path("currencies/", views.CurrencyListAPIView.as_view(), name="currencies"),
] + router.urls
