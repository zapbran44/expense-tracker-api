from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from restapi import models, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

from django.forms.models import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class ExpenseListCreate(ListCreateAPIView):
    serializer_class = serializers.Expense
    queryset = models.Expense.objects.all()
    filterset_fields = ["category", "merchant"]
    permission_classes = [HasAPIKey]


class ExpenseRetrieveDelete(RetrieveDestroyAPIView):
    serializer_class = serializers.Expense
    queryset = models.Expense.objects.all()
    permission_classes = [HasAPIKey]
