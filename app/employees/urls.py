from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from employees import views

router = DefaultRouter()
router.register('', views.Employees, basename='employee')

app_name = 'employee'

urlpatterns = [
    path('', include(router.urls)),
]
