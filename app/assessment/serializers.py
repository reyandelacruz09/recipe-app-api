# from rest_framework import serializers
# from core.models import (
#     Assessment, EmployeeAssessment,
#     Section, Page,
#     EmployeeSection, EmployeePage,
#     QuestionChoice, Question,
#     Choice
# )


# class AssessmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Assessment
#         fields = [
#             'id',
#             'name',
#             'description',
#             'total_page',
#             'total_section',
#             'total_time',
#             'time_limit',
#             'logo',
#             'active',
#         ]


# class SectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Section
#         fields = [
#             'id',
#             'assessment',
#             'name',
#             'description',
#             'total_page',
#             'total_time',
#             'sequence',
#         ]


# class PageSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Page
#         fields = [
#             'id',
#             'section',
#             'name',
#             'description',
#             'description1',
#             'page_no',
#             'page_type',
#             'title',
#             'text',
#             'second_paragraph',
#             'file',
#             'link',
#             'embed',
#             'file_name',
#             'file_type',
#             'timed',
#             'time_limit',
#             'sequence',
#             'video'
#         ]


# class ChoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Choice
#         fields = [
#             'id'
#             'text',
#             'image',
#         ]


# class PageQuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Page
#         fields = [
#             'id',
#             'section',
#             'name',
#             'description1',
#             'description',
#             'page_no',
#             'page_type',
#             'title',
#             'text',
#             'text2',
#             'questions',
#             'file',
#             'link',
#             'embed',
#             'file_name',
#             'file_type',
#             'timed',
#             'time_limit',
#             'sequence',
#             'video'
#         ]

#     questions = serializers.SerializerMethodField('fetch_question')

#     def fetch_question(self, obj):
#         return QuestionSerializer(
#             instance=Question.objects.filter(page=obj),
#             many=True
#         ).data


# class EmployeePageSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = EmployeePage
#         fields = [
#             "id",
#             "page",
#             "current_progress",
#             "completed",
#             "score",
#         ]

#     page = serializers.SerializerMethodField('fetch_page')

#     def fetch_page(self, obj):
#         return PageQuestionSerializer(
#             instance=Page.objects.filter(
#                 id=obj.page.id,
#                 section=obj.page.section
#             ).first(),
#             many=False
#         ).data


# class EmployeeAssessmentSectionSerializer(serializers.ModelSerializer):
#     assessment = AssessmentSerializer()

#     class Meta:
#         model = EmployeeAssessment
#         fields = [
#             'id',
#             'employee',
#             'assessment',
#             'invited_at',
#             'invited_by',
#             'expired_at',
#             'current_progress',
#             'completed',
#             'book_mark',
#             'deleted',
#             'section',
#         ]

#     section = serializers.SerializerMethodField('fetch_section')
#     book_mark = serializers.SerializerMethodField('fetch_book_mark')

#     def fetch_section(self, obj):
#         section_before_certificate = EmployeeSection.objects.filter(
#                 employee_assessment=obj,
#                 section__sequence=int(obj.assessment.total_section) - 1
#             ).first()

#         employee_section = EmployeeSection.objects.filter(
#                 employee_assessment=obj
#             ).order_by('section__sequence')

#         if not section_before_certificate.completed:
#             lat_section = employee_section.reverse()[0]
#             if lat_section.section.is_certificate:
#                 employee_section = employee_section.exclude(
#                     section__sequence=lat_section.section.sequence
#                 )

#         return EmployeeSectionPageSerializer(
#             instance=employee_section,
#             many=True
#         ).data

#     def fetch_book_mark(self, obj):
#         return EmployeePageSerializer(
#             instance=obj.book_mark,
#             many=False
#         ).data


# class EmployeeSectionPageSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = EmployeeSection

#         fields = [
#             'id',
#             'section',
#             'current_progress',
#             'completed',
#             'pages',
#         ]

#     section = serializers.SerializerMethodField('fetch_section')
#     pages = serializers.SerializerMethodField('fetch_pages')

#     def fetch_section(self, obj):
#         return SectionSerializer(
#             instance=Section.objects.filter(
#                 id=obj.section.id
#             ).first(),
#             many=False
#         ).data

#     def fetch_pages(self, obj):
#         return EmployeePageSerializer(
#             instance=EmployeePage.objects.filter(
#                 employee_section=obj,
#                 page__section=obj.section
#             ).order_by('page__sequence'),
#             many=True
#         ).data


# class QuestionChoiceSerializer(serializers.ModelSerializer):
#     # choice = ChoiceSerializer()

#     class Meta:
#         model = QuestionChoice
#         fields = [
#             'id',
#             'question',
#             'choice',
#             'value',
#             'correct_answer',
#             'sequence',
#         ]

#     choice = serializers.SerializerMethodField('fetch_choice')

#     def fetch_choice(self, obj):
#         return "%s" % obj.choice


# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = [
#             'id',
#             'page',
#             'text',
#             'image',
#             'sequence',
#             'choices',
#         ]

#     choices = serializers.SerializerMethodField('fetch_choices')

#     def fetch_choices(self, obj):
#         question_choices = QuestionChoice.objects.filter(
#             question=obj
#         )
#         return QuestionChoiceSerializer(
#             instance=question_choices,
#             many=True
#         ).data
