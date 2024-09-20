from rest_framework import (
    status
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from core import models as core_models
from client import serializers as client_serializer
from rest_framework.response import Response
from client import department as client_dep
from django.db import transaction
from core.core_functions import Core


class DocumentsNews(client_dep.DepartmentViews, Core):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def document_page_list(self, request):
        """
            <GET> /api/client/doc_news/document_page_list/
                ?page=1&page_size=50
        """
        page_size = request.query_params.get("page_size") or 10
        order_by = request.query_params.get("order_by") or 'id'
        order_dir = request.query_params.get("order_dir") or 'desc'
        client = request.query_params.get("client")
        search = request.query_params.get("search") or ""

        order_dir = '' if order_dir == 'asc' else '-'

        paginator = PageNumberPagination()
        paginator.page_size = page_size

        queryset = core_models.Document.objects.filter(
            client__id=int(client)
        ).order_by(
            order_dir + order_by
        )

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        rp = paginator.paginate_queryset(queryset, request)

        ser = client_serializer.DocumentSerializer(
            instance=rp,
            many=True
        ).data

        return paginator.get_paginated_response(
            ser
        )

    @action(methods=['GET'], detail=False)
    def news_page_list(self, request):
        """
            <GET> /api/client/doc_news/news_page_list/
                ?page=1&page_size=50&status=1
        """
        page_size = request.query_params.get("page_size") or 10
        order_by = request.query_params.get("order_by") or 'id'
        order_dir = request.query_params.get("order_dir") or 'desc'
        client = request.query_params.get("client")
        search = request.query_params.get("search")
        order_dir = '' if order_dir == 'asc' else '-'

        paginator = PageNumberPagination()
        paginator.page_size = page_size

        queryset = core_models.News.objects.filter(
            client__id=int(client)
        ).order_by(
            order_dir + order_by
        )

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        rp = paginator.paginate_queryset(queryset, request)

        ser = client_serializer.NewsSerializer(
            instance=rp,
            many=True
        ).data

        return paginator.get_paginated_response(
            ser
        )

    @action(methods=['POST'], detail=False)
    def news_add(self, request):
        """
            <POST> /api/doc_news/news_add/
            request = {
                memo_number: <Integer>
                client:<Instance>
                description:<LongText>
                date_uploaded:<DateTime>
                start:<DateTime>
                end:<DateTime>
                title:<CharField>
                department:<Instance>
                uploaded_by:<Instance>
            }
        """
        data = request.data
        print(data)

        client = self.client_get(
            id=int(data.get('client_id'))
        )

        if not client:
            return Response(
                "Client not found!",
                status=status.HTTP_400_BAD_REQUEST
            )

        user = self.user_get(
            id=int(data.get('user_id'))
        )

        if not user:
            return Response({
                "success": False,
                "message": "User not found"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        depart = self.department_get(
            id=int(data.get('department'))
        )

        if not depart:
            return Response({
                "success": False,
                "message": "Deparment not found"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        news = core_models.News(
            memo_number=self.gen_cntrl_num(type=2),
            client=client,
            description=data.get('description'),
            # date_uploaded=data.get('date_uploaded'),
            start=data.get('start'),
            end=data.get('end'),
            title=data.get('title'),
            department=depart,
            uploaded_by=user
        )

        with transaction.atomic():
            news.save()
            print(self.gen_cntrl_num(type=2))
            print("---")

            for file in request.FILES.getlist('files'):
                nl = core_models.NewsFile(
                    news=news,
                    file=file
                )
                nl.save()

            return Response(
                {
                    "success": True,
                    "message": "News created successfully"
                },
                status=status.HTTP_201_CREATED
            )

    @action(methods=['POST'], detail=False)
    def document_add(self, request, pk=None):
        """
            <POST> /api/client/doc_news/document_add/
            request = {
                client: <Instance>
                department: <Instance>
                date:<DateTime>
                title: <CharField>
                uploaded_by: <Instance>
                description:<LongText>
            }
        """
        data = request.data
        print(data)
        client = self.client_get(
            id=int(data.get('client_id'))
        )

        if not client:
            return Response(
                "Client not found!",
                status=status.HTTP_400_BAD_REQUEST
            )

        user = self.user_get(
            id=int(data.get('user_id'))
        )

        if not user:
            return Response({
                "success": False,
                "message": "User not found"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        depart = self.department_get(
            id=int(data.get('department'))
        )

        if not depart:
            return Response({
                "success": False,
                "message": "Deparment not found"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        doc = core_models.Document(
            client=client,
            control_number=self.gen_cntrl_num(type=1),
            # control_number=Core.gen_cntrl_num(),
            department=depart,
            title=data.get('title'),
            uploaded_by=user,
            description=data.get('description'),
        )

        with transaction.atomic():
            doc.save()
            for file in request.FILES.getlist('files'):
                dl = core_models.DocumentFiles(
                    document=doc,
                    ftp=file
                )
                dl.save()

            return Response(
                {
                    "success": True,
                    "message": "Document created successfully"
                },
                status=status.HTTP_201_CREATED
            )

    @action(methods=['GET'], detail=False)
    def fetch_document_file(slef, request, pk=None):
        """
        <GET> url: api/client/doc_news/fetch_document_file/?file_id=1
        """
        file_id = request.query_params.get("file_id")
        document_file = core_models.DocumentFiles.objects.filter(
            document__id=file_id
        )

        if document_file:
            return Response(
                {
                    "success": True,
                    "data": client_serializer.DocumentFilesSerializer(
                        instance=document_file,
                        many=True
                    ).data
                }, status=status.HTTP_200_OK
            )
