from rest_framework import (
    status
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import (
    Department
)
from client import serializers
from rest_framework.pagination import PageNumberPagination
from core import models as core_models
from rest_framework.decorators import action
from client import serializers as client_serializer
from rest_framework.response import Response
from client import views as client_view


class DepartmentViews(client_view.ClientView):
    serializer_class = serializers.DepartmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Department.objects.all()

    @classmethod
    def department_get(cls, id):
        return Department.objects.filter(
            id=id
        ).first()

    @action(methods=['GET'], detail=False)
    def department_page_list(self, request):
        """
            <GET> /api/client/department/
            department_page_list/?page=1&page_size=50&status=1
        """
        page_size = request.query_params.get("page_size") or 10
        order_by = request.query_params.get("order_by") or 'id'
        order_dir = request.query_params.get("order_dir") or 'desc'
        client_id = request.query_params.get("client")
        search = request.query_params.get("search")

        order_dir = '' if order_dir == 'asc' else '-'

        paginator = PageNumberPagination()
        paginator.page_size = page_size

        client = self.client_get(
            id=int(client_id)
        )

        if not client:
            return Response(
                "Client not found!",
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = core_models.Department.objects.filter(
            client=client
        ).order_by(
            order_dir + order_by
        )

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        rp = paginator.paginate_queryset(queryset, request)

        ser = client_serializer.DepartmentSerializer(
            instance=rp,
            many=True
        ).data

        return paginator.get_paginated_response(
            ser
        )

    @action(methods=['GET'], detail=True)
    def department_list(self, request, pk=None):
        """
            <GET> /api/client/department/<client_id>/
            department_list/
        """
        client = self.client_get(
            id=pk
        )

        if not client:
            return Response(
                "Client not found!",
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "success": True,
            "data": client_serializer.DepartmentSerializer(
                instance=core_models.Department.objects.filter(
                    client=client
                ),
                many=True
            ).data,
        }, status=status.HTTP_200_OK)
