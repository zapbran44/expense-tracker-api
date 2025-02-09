from django.urls import path
from restapi import views

app_name = "restapi"  # ✅ Needed when using namespace

urlpatterns = [
    path("expenses/", views.ExpenseListCreate.as_view(), name="expense-list-create"),
]
