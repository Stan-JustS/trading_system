from django.test import TestCase
from django.db import models
from .models import Stock, Order

class TradingTests(TestCase):
    def setUp(self):
        self.stock = Stock.objects.create(name='AAPL', price=150.00)
        Order.objects.create(stock=self.stock, quantity=10, price=150.00, order_type='BUY')

    def test_portfolio_value(self):
        total = Order.objects.filter(order_type='BUY').aggregate(
            total_value=models.Sum(models.F('quantity') * models.F('price'))
        )['total_value']
        self.assertEqual(total, 1500.00)