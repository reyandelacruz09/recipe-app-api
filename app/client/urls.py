from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from client import (
    department,
    notification,
    views,
    documentsAndNews
)

router = DefaultRouter()
router.register('client_api', views.ClientView, basename='client_api')
router.register(
    'department',
    department.DepartmentViews,
    basename='department'
)
router.register(
    'notification',
    notification.NotificationViews,
    basename='notification'
)
router.register(
    'doc_news',
    documentsAndNews.DocumentsNews,
    basename='doc_news'
)

app_name = 'client'

urlpatterns = [
    path('', include(router.urls)),
]
