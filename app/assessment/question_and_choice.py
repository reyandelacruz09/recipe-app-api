import csv
import codecs
from rest_framework import (
    viewsets,
    status
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from core import models as core_models
# import re


class QuestionAndChoiceView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False)
    def upload_question_choice(self, request, pk=None):
        """ url:api/assessment/question_and_choice/upload_question_choice/ """
        data = request.data
        file = data.get('file')
        reader = csv.DictReader(
            codecs.iterdecode(
                file,
                "utf-8"
            ),
            delimiter=","
        )
        page = core_models.Page.objects.filter(
            id=data.get('page_id')
        ).first()

        list_data = list(reader)
        with transaction.atomic():
            for key, ld in enumerate(list_data, start=1):
                exist_question = core_models.Question.objects.filter(
                    page=page,
                    text=ld.get('questions'),
                    sequence=key
                )
                if not exist_question:
                    new_question = core_models.Question(
                        page=page,
                        text=ld.get('questions'),
                        sequence=key
                    )
                    new_question.save()

                    for i in range(len(ld) - 1):
                        i = i + 1
                        row = "choice" + str(i)

                        if ld.get(row):
                            choice = core_models.Choice.objects.filter(
                                text=ld.get(row),
                            ).first()

                            if not choice:

                                choice = core_models.Choice(
                                    text=ld.get(row),
                                )
                                choice.save()

                            question_choice = core_models.QuestionChoice(
                                question=new_question,
                                choice=choice
                            )

                            question_choice.save()

                            if ld.get('correct') == row:
                                question_choice.correct_answer = True
                                question_choice.save()

        return Response({
                "success": True,
                "data": "Successfully upload Question and Choice"
            }, status=status.HTTP_200_OK)
