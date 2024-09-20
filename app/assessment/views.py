# from rest_framework import (
#     viewsets,
#     status
# )
# from rest_framework.response import Response
# from django.db.models import (
#     Q,
#     Count,
# )
# from rest_framework.decorators import action
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from employees import serializers as emp_serializers
# import datetime
# import pytz
# utc = pytz.UTC


# class AssessmentView(viewsets.ModelViewSet):
#     serializer_class = ass_serializers.AssessmentSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """url:/api/assessment/"""
#         return Assessment.objects.all()

#     @action(methods=['GET'], detail=True)
#     def employee_assessment_detailed(self, request, pk=None):
#         return Response({
#             "success": True,
#             "data": emp_serializers.EmployeeAssessmentSerializerV2(
#                 instance=EmployeeAssessment.objects.filter(
#                     id=pk
#                 ).first(),
#                 many=False
#             ).data,
#         }, status=status.HTTP_200_OK)

#     @action(methods=['GET'], detail=True)
#     def employee_assessment(self, request, pk=None):
#         """
#             url:/api/assessment/<employee_Id>/examination_assessment/
#         """
#         count_assessment_completed = 0
#         count_assessment_expired = 0
#         count_course_to_do = 0
#         employee = Employee.objects.filter(
#             id=pk
#         ).first()

#         if not employee:
#             return Response(
#                 "Employee not found!",
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         employee_assessment = EmployeeAssessment.objects.filter(
#             employee=employee
#         )
#         for ea in employee_assessment:
#             count_current_progress = 0
#             if ea.completed:
#                 count_assessment_completed += 1
#             if not ea.completed:
#                 if ea.expired_at < utc.localize(datetime.datetime.now()):
#                     count_assessment_expired += 1
#                 else:
#                     count_course_to_do += 1

#             for es in EmployeeSection.objects.filter(
#                     employee_assessment=ea
#             ).values(
#                 "employee_assessment",
#                 "current_progress",
#             ):
#                 count_current_progress += es.get('current_progress')

#             ea.current_progress = count_current_progress
#             if ea.assessment.total_page == int(count_current_progress):
#                 if not ea.completed:
#                     ea.completed = \
#                         datetime.datetime.today()
#             ea.save()

#         employee.course_to_do = count_course_to_do
#         employee.overdue_course = count_assessment_expired
#         employee.completed_course = count_assessment_completed
#         employee.save()

#         return Response({
#             "success": True,
#             "data": emp_serializers.EmployeeAssessmentSerializerV2(
#                 instance=employee_assessment,
#                 many=True
#             ).data,
#         }, status=status.HTTP_200_OK)

#     @action(methods=['GET'], detail=True)
#     def employee_assessment_section(self, request, pk=None):
#         """
#             url:/api/assessment/<employee_assessment>/employee_assessment_section/
#         """
#         employee_assessment = EmployeeAssessment.objects.filter(
#             id=pk
#         ).first()

#         for ep in EmployeePage.objects.filter(
#             employee_section__employee_assessment=employee_assessment
#         ).values(
#             "employee_section",
#             "employee_section__section__total_page"
#         ).annotate(
#             count_completed=Count("completed")
#         ):
#             employee_section = EmployeeSection.objects.filter(
#                 id=ep.get('employee_section')
#             ).first()

#             employee_section.current_progress = ep.get('count_completed')

#             if int(ep.get(
#                     'employee_section__section__total_page'
#             )) == int(ep.get(
#                 'count_completed'
#             )):
#                 if not employee_section.completed:
#                     employee_section.completed = datetime.datetime.today()

#             employee_section.save()

#         return Response({
#             "success": True,
#             "data": ass_serializers.EmployeeAssessmentSectionSerializer(
#                 instance=employee_assessment,
#                 many=False
#             ).data,
#         }, status=status.HTTP_200_OK)

#     @action(methods=['GET'], detail=True)
#     def employee_page_detailed(self, request, pk=None):
#         """
#             url:/api/assessment/<employee_page>/employee_page_detailed/
#         """
#         employee_page = EmployeePage.objects.filter(
#                     id=pk
#                 ).first()

#         if not employee_page:
#             return Response(
#                 "Employee Page not found!",
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if not employee_page.completed:
#             employee_page.completed = datetime.datetime.today()

#         employee_page.save()

#         employee_assessment = EmployeeAssessment.objects.filter(
#             id=employee_page.employee_section.employee_assessment.id
#         ).first()

#         if employee_page.page.page_type == Page.CERTIFICATE:
#             employee_assessment.completed = datetime.datetime.today()

#         if not employee_assessment.started:
#             employee_assessment.started = datetime.datetime.today()
#             employee_assessment.save()

#         employee_assessment.book_mark = employee_page
#         employee_assessment.save()

#         employee_page_serializer = ass_serializers.EmployeePageSerializer(
#             instance=employee_page,
#             many=False
#         ).data

#         return Response({
#             "success": True,
#             "data": employee_page_serializer
#         })

#     @action(methods=['POST'], detail=False)
#     def employee_page_next_and_prev(self, request):
#         """
#             url:/api/assessment/employee_page_next_and_prev/
#         """
#         data = request.data
#         employee_assessment = EmployeeAssessment.objects.filter(
#             id=int(data.get('employee_assessment__id'))
#         ).first()

#         filter = Q(
#             employee_section__employee_assessment=employee_assessment
#         )

#         sequence = data.get('sequence')

#         current_employee_page = EmployeePage.objects.filter(
#             employee_section__employee_assessment=employee_assessment,
#             page__sequence=sequence
#         ).first()

#         if data.get('action') == 'next':

#             if int(sequence) == int(
#     employee_assessment.assessment.total_page
# ):
#                 filter &= Q(page__sequence=sequence)
#             else:
#                 filter &= Q(page__sequence=sequence + 1)
#             if not current_employee_page.completed:
#                 current_employee_page.completed = datetime.datetime.today()
#                 current_employee_page.save()

#         if data.get('action') == 'previous':
#             if (sequence - 1) <= 0:
#                 filter &= Q(page__sequence=sequence)
#             else:
#                 filter &= Q(page__sequence=sequence - 1)

#         employee_page = EmployeePage.objects.filter(
#             filter
#         ).first()

#         if int(sequence) == int(employee_assessment.assessment.total_page):
#             if not employee_page.completed:
#                 employee_page.completed = datetime.datetime.today()
#                 employee_page.save()

#         employee_assessment.book_mark = employee_page
#         employee_assessment.save()

#         return Response({
#             "success": True,
#             "data": ass_serializers.EmployeePageSerializer(
#                 instance=employee_page,
#                 many=False
#             ).data
#         })

#     @action(methods=['POST'], detail=False)
#     def reset_employee_assessment(self, request, pk=None):
#         """
#             url:/api/assessment/reset_employee_assessment/
#         """
#         data = request.data

#         employee_assessment = EmployeeAssessment.objects.filter(
#             id=data.get('employee_ass_id')
#         ).first()

#         if not employee_assessment:
#             return Response(
#                 "Employee Assessment not found!",
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         employee_assessment.completed = None
#         employee_assessment.current_progress = 0
#         employee_assessment.save()

#         for es in EmployeeSection.objects.filter(
#             employee_assessment=employee_assessment
#         ):
#             es.completed = None
#             es.current_progress = 0
#             es.save()
#             for ep in EmployeePage.objects.filter(
#                 employee_section=es
#             ):
#                 if ep.page.sequence == 1:
#                     employee_assessment.book_mark = ep
#                     employee_assessment.save()

#                 ep.completed = None
#                 ep.current_progress = 0
#                 ep.save()

#         return Response({
#             "success": True,
#             "message": "Successfully Reset Employee Assessment"
#         })
