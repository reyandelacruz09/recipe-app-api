from django.urls import (
    path,
    include,
)
# from .views import AssessmentView
# from .question_and_choice import QuestionAndChoiceView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('', AssessmentView, basename='assessment')
# router.register(
#     'question_and_choice',
#     QuestionAndChoiceView,
#     basename='question_and_choice'
# )

# app_name = 'assessment'

urlpatterns = [
    path('', include(router.urls)),
]
