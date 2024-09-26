from django.test import TestCase

# Create your tests here.
# orders/tests.py

from django.test import TestCase
from .models import Customer, Order
from rest_framework.test import APIClient

class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="John Doe", code="JD123", phone="+254700000000")

    def test_customer_creation(self):
        self.assertEqual(self.customer.name, "John Doe")
        self.assertEqual(self.customer.code, "JD123")

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="John Doe", code="JD123", phone="+254700000000")
        self.order = Order.objects.create(customer=self.customer, item="Laptop", amount=45000.00)

    def test_order_creation(self):
        self.assertEqual(self.order.item, "Laptop")
        self.assertEqual(self.order.amount, 45000.00)

class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="John Doe", code="JD123", phone="+254700000000")

    def test_create_order(self):
        response = self.client.post('/api/orders/', {'customer': self.customer.id, 'item': 'Laptop', 'amount': 45000.00})
        self.assertEqual(response.status_code, 201)
