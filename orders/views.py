# orders/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from .utils import send_sms_notification

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request):
        customers = self.get_queryset()
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            customer = self.get_object()
        except Customer.DoesNotExist:
            raise NotFound(f"Customer with id {pk} not found.")
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            customer = self.get_object()
        except Customer.DoesNotExist:
            raise NotFound(f"Customer with id {pk} not found.")
        serializer = self.get_serializer(customer, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            customer = self.get_object()
        except Customer.DoesNotExist:
            raise NotFound(f"Customer with id {pk} not found.")
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



    def list(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            order = self.get_object()
        except Order.DoesNotExist:
            raise NotFound(f"Order with id {pk} not found.")
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            order = self.get_object()
        except Order.DoesNotExist:
            raise NotFound(f"Order with id {pk} not found.")
        serializer = self.get_serializer(order, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            order = self.get_object()
        except Order.DoesNotExist:
            raise NotFound(f"Order with id {pk} not found.")
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order = serializer.save()  # Save the new order

            # Get customer info
            customer = order.customer
            customer_phone = customer.phone

            # Prepare the message
            message = f"Hi {customer.name}, your order for {order.item} worth {order.amount} has been successfully placed."

            # Send SMS notification
            send_sms_notification(customer_phone, message)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
