from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from restapi import models
from django.forms.models import model_to_dict

# Create your views here.
class ExpenseListCreate(APIView):
    def get(self, request):
        expenses = models.Expense.objects.all()
        expenses_list = [model_to_dict(expense) for expense in expenses]
        return Response(expenses_list, status=200)  # ✅ Now returns valid JSON

    def post(self, request):
        amount = request.data["amount"]
        merchant = request.data["merchant"]
        description = request.data["description"]
        category = request.data["category"]

        expense = models.Expense.objects.create(
            amount=amount, merchant=merchant, description=description, category=category
        )
        return Response(model_to_dict(expense), status=201)
