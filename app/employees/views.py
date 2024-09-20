from rest_framework import (
    status
)
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from employees import serializers
from core import models as core_model
# from django.core.files.base import File
from .core import Core as emp_core
from user.core import Core as user_core
from client.core import Core as client_core
from core.core_functions import Core as super_core
from rest_framework import (
    viewsets
)


class Employees(
    viewsets.ModelViewSet,
    emp_core,
    client_core,
    super_core,
    user_core
):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=True)
    def employee_detailed(self, request, pk=None):
        """
            url:/api/employee/<user_id>/employee_detailed/
        """

        employee = core_model.Employee.objects.filter(
            user__id=pk
        ).first()

        if not employee:
            return Response(
                "Employee not found!",
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "success": True,
            "data": serializers.EmployeeSerializer(
                instance=employee,
                many=False
            ).data,
        }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def employee_list(self, request, pk=None):
        """
           url:/api/employee/employee_list/?client_id=1
        """
        client_id = int(request.query_params.get("client_id"))

        client = core_model.Client.objects.filter(id=client_id).first()

        if not client:
            return Response(
                "Client not found!",
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "success": True,
            "data": serializers.EmployeeSerializer(
                instance=core_model.Employee.objects.filter(
                    client=client
                ).exclude(status=core_model.Employee.DELETED),
                many=True
            ).data,
        }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def add_employee(self, request, pk=None):
        """
            url:/api/employee/add_employee/
        """
        data = request.data
        client = core_model.Client.objects.filter(
            id=int(data.get('client_id'))
        ).first()

        if not client:
            return Response(
                'Client not found!',
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            if data.get('step') == 1:
                """
                    payload = {
                        step:1,
                        email:<CharField>,
                        first_name:<CharField>,
                        middle_name:<CharField>,
                        last_name:<CharField>,
                        client_id:<Instance>,
                        employee_id:<CharField>,
                        gender:<Integer>,
                        profile_image:<ImageField>,
                        address_1:<TextField>,
                        address_2:<TextField>,
                        phone_number:<Integer>s,
                        mobile_number:<Integer>,
                        martial_status:<Integer choices>,
                        birthday:<DateField>,
                        cpioe:<CharField>,
                        cpioe_contact_no:data.get('cpioe_contact_no'),
                    }
                """

                data.pop('step')
                user = self.create_user(
                    email=data.get('email'),
                    first_name=data.get('first_name'),
                    middle_name=data.get('middle_name'),
                    last_name=data.get('last_name'),
                    username=data.get('email')
                )[0]

                [
                    data.pop(p) for p in [
                        'email',
                        'first_name',
                        'middle_name',
                        'last_name'
                    ]
                ]

                self.save_employee(
                    user=user,
                    client=client,
                    **data,
                    creation_step=2
                )

            elif data.get('step') == 2:
                """
                    payload = {
                        id=:1,
                        educ_back:
                        [
                            {
                                "type": 1,
                                "name": <Character>
                                "date_graduated": <DateField>
                                "address": <TextField>
                                "degree": <CharField>
                            }
                        ]
                    }
                """
                data.pop('step')
                emp = self.get_emp(
                    id=data.get('id')
                ).first()

                if not emp:
                    return Response(
                        'Employee not found!',
                        status=status.HTTP_400_BAD_REQUEST
                    )

                for eb in data.get('educ_back'):
                    e_back = core_model.EducBackGround.objects.filter(
                        educ_type=eb.get('educ_type'),
                        employee=emp
                    ).first()

                    if not e_back:
                        self.save_educ_back(
                            emp=emp,
                            **eb
                        )

                emp.creation_step = 3
                emp.save()

            elif data.get('step') == 3:
                """
                    payload = {
                        step:3,
                        id=:1,
                        client_id:1,
                        sss_no:<CharField>,
                        phil_no:<CharField>,
                        tin_no:<CharField>,
                        pagibig_no:<CharField>,
                        creation_step:<Integer>,
                    }
                """
                data.pop('step')
                emp = self.get_emp(
                    id=data.get('id')
                )

                if not emp:
                    return Response(
                        'Employee not found!',
                        status=status.HTTP_400_BAD_REQUEST
                    )
                emp.update(
                    **data
                )

            elif data.get('step') == 4:
                """
                    payload = {
                        "step": <Integer>,
                        "client_id":<ForeignKey>,
                        "id": <ForeignKey>,
                        "level": <ForeignKey>,
                        "job_title": <ForeignKey>,
                        "department": <ForeignKey>,
                        "office_location": <ForeignKey>,
                        "employee_status": <Integer>,
                        "work_arrangement":<Integer>,
                        "date_hired": <DateField>,
                        "benefits": [
                            {
                                "benefit": <ForeignKey>,
                                "amount": <Decimal>
                                "term": <Integer>,
                                "start_date": <DateField>
                            },
                        ]
                    }
                """
                data.pop('step')
                emp = self.get_emp(
                    id=data.get('id')
                )
                data.pop('id')
                if not emp:
                    return Response(
                        'Employee not found!',
                        status=status.HTTP_400_BAD_REQUEST
                    )

                level = self.get_level(
                    id=data.pop('level')
                )

                if not level:
                    return Response(
                        'Level not found!',
                        status=status.HTTP_400_BAD_REQUEST
                    )

                job_title = self.get_jobtitle(
                    id=data.pop('job_title')
                )

                if not job_title:
                    return Response(
                        'Jobtitle not found!',
                        status=status.HTTP_400_BAD_REQUEST
                    )

                department = self.get_department(
                    id=data.pop('department')
                )

                if not department:
                    return Response(
                        'Department not found!',
                        status=status.HTTP_400_BAD_REQUEST
                    )

                off_loc = self.get_off_location(
                    id=data.pop('office_location')
                )

                if not off_loc:
                    return Response(
                        'Office location not found!',
                        status=status.HTTP_400_BAD_REQUEST
                    )

                emp.update(
                    level=level,
                    job_title=job_title,
                    department=department,
                    office_location=off_loc
                )

                for bf in data.get('benefits'):
                    bft = self.get_client_benefits(
                        client=client,
                        id=bf.pop('benefit')
                    ).first()

                    if not bft:
                        return Response(
                            'Client Benefits not found!',
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    eb = self.emp_benefits(
                        benefits=bft,
                        employee=emp.first()
                    )

                    if not eb:
                        self.save_emp_benefits(
                            benefits=bft,
                            employee=emp.first(),
                            **bf
                        )

            elif data.get('step') == 5:
                """
                    {
                        "step": <Integer>,
                        "client_id":<ForeignKey>,
                        "id": <ForeignKey>,
                        benefits": [
                            {
                                "com": <ForeignKey>,
                                "count": <Decimal>
                                "term": <Integer>,
                                "availabity": <Integer>
                            },
                        ]
                    }
                """
                data.pop('step')
                emp = self.get_emp(
                    id=data.get('id')
                ).first()
                data.pop('id')

                if not emp:
                    return Response(
                        'Employee not found!',
                        status=status.HTTP_400_BAD_REQUEST
                    )

                for com in data.get('compensation'):
                    c_com = self.get_client_compensation(
                        client=client,
                        id=com.get('com')
                    ).first()
                    com.pop('com')

                    ec = self.emp_compensation(
                        employee=emp,
                        compensation=c_com
                    ).first()

                    if not ec:
                        self.save_emp_compensation(
                            employee=emp,
                            compensation=c_com,
                            **com
                        )

            return Response(
                "Successfully added Employee",
                status=status.HTTP_200_OK
            )

    @action(methods=['DELETE'], detail=True)
    def delete_employee(self, request, pk=None):
        """
            url:/api/employee/delete_employee/
        """

        employee = self.get_emp(
            id=pk
        ).first()

        if not employee:
            return Response(
                'User not found!',
                status=status.HTTP_400_BAD_REQUEST
            )

        employee.status = core_model.Employee.status = \
            core_model.Employee.DELETED
        employee.save()

        return Response(
            "Successfully deleted employee",
            status=status.HTTP_200_OK
        )

    @action(methods=['PUT'], detail=True)
    def employee_detail_edit(self, request, pk=None):
        """
            url:/api/employee/<employee_id>/employee_detail_edit/
        """
        data = request.data

        employee = self.get_emp(
            id=pk
        )

        if not employee:
            return Response(
                'Employee not found!',
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            employee.update(**data)

            return Response({
                "success": True,
                "message": "Successfully updated employee detail",
                "data": serializers.EmployeeSerializer(
                    instance=employee,
                    many=False
                ).data,
            }, status=status.HTTP_200_OK)
