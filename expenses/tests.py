from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ExpenseIncome

class ExpenseIncomeAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.superuser = User.objects.create_superuser(username="admin", password="adminpass")

        self.login_url = "/api/auth/login/"
        self.expenses_url = "/api/expenses/"

        self.user_token = self.get_token("testuser", "testpass")
        self.superuser_token = self.get_token("admin", "adminpass")

    def get_token(self, username, password):
        response = self.client.post(self.login_url, {"username": username, "password": password})
        return response.data["access"]

    def auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_expense_flat_tax(self):
        self.auth(self.user_token)
        payload = {
            "title": "Flat Tax Test",
            "description": "Test Desc",
            "amount": 100.00,
            "transaction_type": "debit",
            "tax": 10.00,
            "tax_type": "flat"
        }
        response = self.client.post(self.expenses_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data["total"]), 110.00)

    def test_create_expense_percentage_tax(self):
        self.auth(self.user_token)
        payload = {
            "title": "Percentage Tax Test",
            "amount": 100.00,
            "transaction_type": "debit",
            "tax": 10.00,
            "tax_type": "percentage"
        }
        response = self.client.post(self.expenses_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data["total"]), 110.00)

    def test_zero_tax(self):
        self.auth(self.user_token)
        payload = {
            "title": "Zero Tax Test",
            "amount": 100.00,
            "transaction_type": "credit",
            "tax": 0.00
        }
        response = self.client.post(self.expenses_url, payload, format="json")
        self.assertEqual(float(response.data["total"]), 100.00)

    def test_user_can_only_see_own_expenses(self):
        # Create one expense as testuser
        self.auth(self.user_token)
        self.client.post(self.expenses_url, {
            "title": "My Expense",
            "amount": 100,
            "transaction_type": "debit"
        }, format="json")

        # Now log in as superuser and verify access to all
        self.auth(self.superuser_token)
        response = self.client.get(self.expenses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 1)

        # Now log in as testuser and ensure only own data visible
        self.auth(self.user_token)
        response = self.client.get(self.expenses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_unauthenticated_access_denied(self):
        response = self.client.get(self.expenses_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_superuser_can_delete_any_expense(self):
        self.auth(self.user_token)
        post_resp = self.client.post(self.expenses_url, {
            "title": "Deletable",
            "amount": 50,
            "transaction_type": "debit"
        }, format="json")
        expense_id = post_resp.data["id"]

        self.auth(self.superuser_token)
        del_resp = self.client.delete(f"{self.expenses_url}{expense_id}/")
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_others_expense(self):
        self.auth(self.user_token)
        post_resp = self.client.post(self.expenses_url, {
            "title": "Not Yours",
            "amount": 99,
            "transaction_type": "debit"
        }, format="json")
        expense_id = post_resp.data["id"]

        self.auth(self.superuser_token)
        response = self.client.get(f"{self.expenses_url}{expense_id}/")
        self.assertEqual(response.status_code, 200)

        # Create a new user and try deleting that record
        other_user = User.objects.create_user("otheruser", "x@test.com", "otherpass")
        other_token = self.get_token("otheruser", "otherpass")

        self.auth(other_token)
        delete_resp = self.client.delete(f"{self.expenses_url}{expense_id}/")
        self.assertIn(delete_resp.status_code, [403, 404])  
