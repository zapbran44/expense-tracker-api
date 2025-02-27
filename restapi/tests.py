from django.test import TestCase
from restapi import models
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey
from rest_framework.test import APIClient

# Create your tests here.
class TestModels(TestCase):
    def test_expense(self):
        expense = models.Expense.objects.create(
            amount=249.99,
            merchant="amazon",
            description="anc headphones",
            category="music",
        )
        inserted_expense = models.Expense.objects.get(pk=expense.id)
        self.assertEqual(249.99, inserted_expense.amount)
        self.assertEqual("amazon", inserted_expense.merchant)
        self.assertEqual("anc headphones", inserted_expense.description)
        self.assertEqual("music", inserted_expense.category)


class TestViews(TestCase):
    def setUp(self):
        # User.objects.create_user("test1234", "test1234@example.com", "test1234")
        # self.client.login(username="test1234", password="test1234")
        api_key, key = APIKey.objects.create_key(name="expense-service")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Api-Key {key}")

    def test_expense_create(self):
        payload = {
            "amount": 50.0,
            "merchant": "AT&T",
            "description": "cell phone subscription",
            "category": "utilities",
        }
        res = self.client.post(
            reverse("restapi:expense-list-create"), payload, format="json"
        )
        self.assertEqual(201, res.status_code)
        json_res = res.json()
        self.assertEqual(payload["amount"], json_res["amount"])
        self.assertEqual(payload["merchant"], json_res["merchant"])
        self.assertEqual(payload["description"], json_res["description"])
        self.assertEqual(payload["category"], json_res["category"])
        self.assertIsInstance(json_res["id"], int)

    def test_expense_list(self):
        res = self.client.get(reverse("restapi:expense-list-create"), format="json")
        self.assertEqual(200, res.status_code)
        json_res = res.json()
        self.assertIsInstance(json_res, list)
        expenses = models.Expense.objects.all()
        self.assertEqual(len(expenses), len(json_res))

    def test_expense_create_required_fields_missing(self):
        payload = {
            "merchant": "AT&T",
            "description": "cell phone subscription",
            "category": "utilities",
        }
        res = self.client.post(
            reverse("restapi:expense-list-create"), payload, format="json"
        )
        self.assertEqual(400, res.status_code)
        json_res = res.json()
        print(json_res)
        # self.assertIn("error", json_res)

    def test_expense_retrieve(self):
        expense = models.Expense.objects.create(
            amount=300, merchant="George", description="loan", category="transfer"
        )
        res = self.client.get(
            reverse("restapi:expense-retrieve-delete", args=[expense.id]), format="json"
        )
        self.assertEqual(200, res.status_code)
        json_res = res.json()
        self.assertEqual(expense.id, json_res["id"])
        self.assertEqual(expense.amount, json_res["amount"])
        self.assertEqual(expense.merchant, json_res["merchant"])
        self.assertEqual(expense.description, json_res["description"])
        self.assertEqual(expense.category, json_res["category"])

    def test_expense_delete(self):
        expense = models.Expense.objects.create(
            amount=400, merchant="John", description="loan", category="transfer"
        )
        res = self.client.delete(
            reverse("restapi:expense-retrieve-delete", args=[expense.id]), format="json"
        )
        self.assertEqual(204, res.status_code)
        self.assertFalse(models.Expense.objects.filter(pk=expense.id).exists())

    def test_list_expense_filter_by_merchant(self):
        amazon_expense = models.Expense.objects.create(
            amount=100, merchant="amazon", description="sunglasses", category="fashion"
        )
        ebay_expense = models.Expense.objects.create(
            amount=200, merchant="ebay", description="watch", category="fashion"
        )
        url = "/api/expenses?merchant=amazon"
        res = self.client.get(url, format="json")
        self.assertEqual(200, res.status_code)
        json_res = res.json()
        self.assertEqual(1, len(json_res))
        self.assertEqual(amazon_expense.id, json_res[0]["id"])
        self.assertEqual(amazon_expense.amount, json_res[0]["amount"])
        self.assertEqual(amazon_expense.merchant, json_res[0]["merchant"])
        self.assertEqual(amazon_expense.description, json_res[0]["description"])
        self.assertEqual(amazon_expense.category, json_res[0]["category"])

    def test_list_expense_filter_by_category(self):
        amazon_expense = models.Expense.objects.create(
            amount=100, merchant="amazon", description="sunglasses", category="fashion"
        )
        ebay_expense = models.Expense.objects.create(
            amount=200, merchant="ebay", description="watch", category="fashion"
        )
        groceries_expense = models.Expense.objects.create(
            amount=30, merchant="walmart", description="beer", category="groceries"
        )
        url = "/api/expenses?category=fashion"
        res = self.client.get(url, format="json")
        self.assertEqual(200, res.status_code)
        json_res = res.json()
        self.assertEqual(2, len(json_res))
