from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Stock, Order
from .serializers import StockSerializer, OrderSerializer
from django.db.models import Sum, F

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    @action(detail=True, methods=['get'])
    def value(self, request, pk=None):
        stock = self.get_object()
        total = Order.objects.filter(stock=stock, order_type='BUY').aggregate(
            total_value=Sum(F('quantity') * F('price'))
        )['total_value'] or 0
        return Response({'stock': stock.name, 'total_invested': total})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['get'])
    def portfolio_value(self, request):
        total = Order.objects.filter(order_type='BUY').aggregate(
            total_value=Sum(F('quantity') * F('price'))
        )['total_value'] or 0
        return Response({'total_portfolio_value': total})