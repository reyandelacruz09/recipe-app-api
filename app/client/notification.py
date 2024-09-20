from rest_framework import (
    status
)
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import (
    Employee,
    Notification
)
from django.db import transaction
from client import views as client_view


class NotificationViews(client_view.ClientView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False)
    def add_notification(self, request, pk=None):
        """
            http://localhost:8000/api/notification/add_notification/
        """
        data = request.data

        employee = Employee.objects.filter(
            id=int(data.get("employee_id"))
        ).first()

        if not employee:
            return Response(
                "Employee not found!",
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            notification = Notification(
                sender=employee.user,
                to_client=employee.client,
                subject=data.get('subject'),
                message=data.get('message')
            )
            notification.save()

            if data.get('file'):
                notification.file = data.get('file')
                notification.save()

            return Response({
                "success": True,
                "data": "Thank you! Your feedback has been sent",
            }, status=status.HTTP_200_OK)
