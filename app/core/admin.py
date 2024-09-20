"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.models import LogEntry

from core import models


class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    ]

    readonly_fields = (
        'content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    )
    search_fields = [
        'object_id',
        'object_repr',
        'change_message'
    ]

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ['first_name', 'last_name', 'email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal Info'), {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
            )}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'), {'fields': ('last_login',)},
        ),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'first_name',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
            }),
    )


class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'memo_number',
        'title',
        'date_uploaded',
        'start',
        'end',
        'ftp'
    ]

    search_field = [
        'title',
        'memo_number',
    ]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'employee_id',
        'first_name',
        'last_name',
        'email',
        'client',
        'job_title',
        'employee_status',
        'department',
        'status',
    ]

    raw_id_fields = ['user']

    search_fields = [
        'employee_id',
        'user__first_name',
        'user__last_name',
        'client__company_name',
    ]

    list_filter = (
        ('client', admin.RelatedFieldListFilter),
    )

    def first_name(self, obj):
        result = ''
        if obj.user:
            result = obj.user.first_name
        return result

    def last_name(self, obj):
        result = ''
        if obj.user:
            result = obj.user.last_name
        return result

    def email(self, obj):
        result = ''
        if obj.user:
            result = obj.user.email
        return result

    first_name.short_description = "First name"
    last_name.short_description = "Last name"
    email.short_description = "Email"


class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company_name',
        'company_url',
        'address_1',
        'phone_number',
        'mobile_number',
    ]

    search_fields = [
        'company_name',
        'company_url',
        'address_1'
    ]


class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'employee',
        'date',
        'image',
        'task_image',
        'remarks',
        'site_location'
    ]

    raw_id_fields = ['employee']

    search_fields = [
        'employee__employee_id',
        'employee__user__first_name',
        'employee__user__last_name',
    ]


class AssessmentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description',
        'total_section',
        'total_time',
        'time_limit',
        'active'
    ]

    search_fields = [
        "name",
    ]


class ClientAssessmentAdmin(admin.ModelAdmin):
    list_display = [
        'client',
        'assessment',
    ]

    search_fields = [
        'client__company_name',
    ]

    list_filter = (
        ('client', admin.RelatedFieldListFilter),
    )

    def client(self, obj):
        return obj.company_name

    client.short_description = 'Client'


class SectionAdmin(admin.ModelAdmin):
    list_display = [
        'assessment_name',
        'description',
        'sequence',
        'total_page',
        'total_time',
    ]

    search_fields = [
        "name",
    ]

    list_filter = (
        ('assessment', admin.RelatedFieldListFilter),
    )

    def assessment_name(self, obj):
        return obj.assessment.name

    assessment_name.short_description = "Assessment"


class PageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'section',
        'name',
        'embed',
        'sequence',
        'page_no',
        'page_type',
        'time_limit',
    ]

    search_fields = [
        'name',
    ]

    list_filter = (
        ('section__assessment', admin.RelatedFieldListFilter),
    )

    def section_name(self, obj):
        return obj.section.name

    section_name.short_description = "Section"


class EmployeeAssessmentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'assessment_name',
        'employee_name',
        'invited_at',
        'invited_by',
        'started',
        'expired_at',
        'deleted',
        'completed',
    ]

    search_fields = [
        "assessment__name",
    ]

    def employee_name(self, obj):
        return "%s %s" % (
            obj.employee.user.first_name,
            obj.employee.user.last_name
        )

    employee_name.short_description = "Employee"

    def assessment_name(self, obj):
        return obj.assessment.name

    assessment_name.short_description = "Assessment"


class EmployeeSectionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'employee',
        'section',
        'current_progress',
        'completed',
    ]
    search_fields = [
        'section__assessment__name'
    ]

    list_filter = (
        ('employee_assessment__assessment', admin.RelatedFieldListFilter),
    )

    def employee(self, obj):
        return "%s %s" % (
            obj.employee_assessment.employee.user.first_name,
            obj.employee_assessment.employee.user.last_name
        )

    employee.short_description = "Employee"


class EmployeePageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'employee',
        'page',
        'current_progress',
        'completed',
        'score',
    ]
    search_fields = [
        'section__assessment__name'
    ]

    list_filter = (
        ('employee_section__employee_assessment__assessment',
         admin.RelatedFieldListFilter),
    )

    def employee(self, obj):
        return "%s %s" % (
            obj.employee_section.employee_assessment.employee.user.first_name,
            obj.employee_section.employee_assessment.employee.user.last_name
        )

    employee.short_description = "Employee"


class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'page',
        'text',
        'image',
        'sequence'
    ]

    search_fields = [
        'text',
        'page__name',
        'page__title'
    ]

    list_filter = (
        ('page__section__assessment',
         admin.RelatedFieldListFilter),
    )


class ChoiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'text',
        'image',
    ]

    search_fields = [
        'id',
        'text'
    ]


class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = [
        'question',
        'choice',
        'value',
        'sequence',
        'correct_answer',
    ]

    search_fields = [
        'id',
        'question__text',
    ]

    list_filter = (
        ('question__page', admin.RelatedFieldListFilter),
    )


# class AnswerAdmin(admin.ModelAdmin):
#     list_display = [
#         'employee',
#         'question_choice',
#         'time_consume',
#     ]
#
#     search_fields = [
#         'employee__user__first_name',
#         'employee__user__last_name'
#     ]
#
#
# class ScoreAdmin(admin.ModelAdmin):
#     list_display = [
#         'employee_page',
#         'score',
#         'average_time'
#     ]
#
#     search_fields = [
#         'employee_page__employee__user__first_name',
#         'employee_page__employee__user__last_name'
#     ]


class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'sender',
        'receiver',
        'from_client',
        'to_client',
        'subject',
        'is_seen',
        'message',
        'created_at'
    ]

    search_fields = [
        'to_client__company_name',
        'receive__first_name',
        'receive__last_name'
        'sender__first_name',
        'sender__last_name',
    ]

    list_filter = (
        ('to_client', admin.RelatedFieldListFilter),
    )


class BadgeAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'image1',
        'image2',
    ]

    search_fields = [
        'title',
    ]


class AssessmentBadgeAdmin(admin.ModelAdmin):
    list_display = [
        'assessment',
        'badge',
    ]

    search_fields = [
        'assessment__name'
    ]

    list_filter = (
        ('assessment', admin.RelatedFieldListFilter),
    )


class EmployeeBadgeAdmin(admin.ModelAdmin):
    list_display = [
        'employee',
        'badge',
        'completed'
    ]

    search_fields = [
        'employee__user__first_name',
        'employee__user__last_name'
    ]

    list_filter = (
        ('badge', admin.RelatedFieldListFilter),
    )


class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'control_number',
        'client',
        'department',
        'date',
        'title',
        'status',
    ]

    search_fields = [
        'control_number',
        'title'
    ]

    list_filter = (
        ('client', admin.RelatedFieldListFilter),
    )


class DocumentFilesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'document',
        'ftp',
        'link',
        'date_uploaded',
        'version',
    ]

    search_fields = [
        'document__control_number',
        'document___title'
    ]


class DepartmentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'representative',
        'info',
    ]

    search_fields = [
        'name',
    ]


class NewsFileAdmin(admin.ModelAdmin):
    list_display = [
        'news',
        'file',
    ]

    search_fields = [
        'news__title',
        'news__memo_number',
    ]


class JobTitleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'client',
        'name',
    ]

    search_fields = [
        'name',
    ]

    list_filter = (
        ('client', admin.RelatedFieldListFilter),
    )


class LevelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'client',
        'name',
    ]

    search_fields = [
        'name',
    ]

    list_filter = (
        ('client', admin.RelatedFieldListFilter),
    )


class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'client',
        'name',
    ]

    search_fields = [
        'name',
    ]

    list_filter = (
        ('client', admin.RelatedFieldListFilter),
    )


class EducBackGroundAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'employee',
        'school_name',
        'date_graduated',
        'degree',
        'address',
    ]

    search_fields = [
        'employee__user__first_name',
        'employee__user__last_name',
    ]


class ClientCompensationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'client',
        'name',
        'type',
    ]

    list_filter = (
        ('client', admin.RelatedFieldListFilter),
    )


class ClientBenefitsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'client',
        'name',
    ]

    list_filter = (
        ('client', admin.RelatedFieldListFilter),
    )


class EmployeeBenefitsAdmin(admin.ModelAdmin):
    list_display = [
        'benefits',
        'employee',
        'amount',
        'term',
        'start_date',
    ]

    list_filter = (
        ('employee', admin.RelatedFieldListFilter),
    )


class EmployeeCompensationAdmin(admin.ModelAdmin):
    list_display = [
        'employee',
        'compensation',
        'count',
        'type',
        'term',
        'availability',
    ]

    list_filter = (
        ('compensation__client', admin.RelatedFieldListFilter),
    )


class RegionAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]

    search_fields = [
        'name',
    ]


class ProvinceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'region',
    ]

    search_fields = [
        'name',
        'region__name'
    ]


class CityAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'province',
    ]

    search_fields = [
        'name',
        'province__name'
    ]


class BarangayAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

    search_fields = [
        'name',
        'city__name'
    ]


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.News, NewsAdmin)
admin.site.register(models.Document, DocumentAdmin)
admin.site.register(
    models.DocumentFiles,
    DocumentFilesAdmin
)
admin.site.register(
    models.Attendance,
    AttendanceAdmin
)
admin.site.register(
    models.Notification,
    NotificationAdmin
)
admin.site.register(
    models.NewsFile,
    NewsFileAdmin
)
admin.site.register(models.JobTitle, JobTitleAdmin)
admin.site.register(models.Level, LevelAdmin)
admin.site.register(
    models.OfficeLocation,
    OfficeLocationAdmin
)
admin.site.register(
    models.EducBackGround,
    EducBackGroundAdmin
)
admin.site.register(
    models.ClientCompensation,
    ClientCompensationAdmin
)
admin.site.register(
    models.ClientBenefits,
    ClientBenefitsAdmin
)
admin.site.register(
    models.EmployeeBenefits,
    EmployeeBenefitsAdmin
)
admin.site.register(
    models.EmployeeCompensation,
    EmployeeCompensationAdmin
)
admin.site.register(
    models.Region,
    RegionAdmin
)
admin.site.register(
    models.Province,
    ProvinceAdmin
)
admin.site.register(
    models.City,
    CityAdmin
)
admin.site.register(
    models.Barangay,
    BarangayAdmin
)
