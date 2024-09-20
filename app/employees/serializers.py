from rest_framework import serializers
from core import models as core_model
from user import serializers as user_serializer
from client import serializers as client_serializer
# from assessment import serializers as ass_serializer
# from datetime import datetime


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee"""
    user = user_serializer.UserSerializer()
    department = client_serializer.DepartmentSerializer()
    client = client_serializer.ClientSerializer()

    class Meta:
        model = core_model.Employee
        fields = [
            'id',
            'client',
            'user',
            'employee_id',
            'profile_image',
            'gender',
            'date_hired',
            'job_title',
            'address_1',
            'address_2',
            'phone_number',
            'mobile_number',
            'martial_status',
            'birthday',
            'employee_status',
            'user_type',
            'office_location',
            'work_arrangement',
            'department',
            'status',
            'cpioe',
            'cpioe_contact_no',
            'course_to_do',
            'overdue_course',
            'completed_course',
        ]


class EmployeeAttendance(serializers.ModelSerializer):
    class Meta:
        model = core_model.Attendance
        fields = [
            'id',
            'employee',
            'title',
            'start',
            'end',
            'description',
            'color',
        ]

    title = serializers.SerializerMethodField('fetch_title')
    start = serializers.SerializerMethodField('fetch_start')
    end = serializers.SerializerMethodField('fetch_end')
    description = serializers.SerializerMethodField('fetch_description')
    color = serializers.SerializerMethodField('fetch_color')

    def fetch_title(self, obj):
        title_name = ''

        if obj.type == 1:
            title_name = 'TIME IN'

        if obj.type == 2:
            title_name = 'TIME OUT'

        if obj.type == 3:
            title_name = 'LEAVE'

        return title_name

    def fetch_start(self, obj):
        return obj.date

    def fetch_end(self, obj):
        return obj.date

    def fetch_description(self, obj):
        return obj.remarks

    def fetch_color(self, obj):
        color = 'black'

        if obj.type == 1:
            color = 'green'

        if obj.type == 2:
            color = '#2566e8'

        if obj.type == 3:
            color = 'yellow'

        return color
