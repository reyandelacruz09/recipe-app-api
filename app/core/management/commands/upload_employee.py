from django.core.management.base import BaseCommand
from core import models as core_models
from django.db import transaction
import json
from client import (
    department as client_dep,
    core as client_core
)
from user import views as user_view
from datetime import datetime
from user.core import Core as user_core


class Command(
    BaseCommand,
    client_dep.DepartmentViews,
    user_view.UserView,
    client_core.Core,
    user_core
):
    help = """
        Initial Upload
        argument
        --client_id = <INTEGER>
        --type = <STRING> (
            all, department,
            jobtitle, level,
            off_loc
        )
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--client_id', type=int, help=''
        )

    def handle(self, *args, **options):
        cl_id = options['client_id']

        if not cl_id:
            self.stdout.write(self.style.WARNING(
                'Client ID not found!'
            ))
            return False

        client = self.client_get(
            id=int(cl_id)
        )

        if not client:
            self.stdout.write(self.style.WARNING(
                'Client not found!'
            ))
            return False

        with transaction.atomic():
            for emp in json.loads(
                open('core/management/json/employee_list.json').read()
            ):

                # Check if the employee with the
                #  given employee_id already exists
                if not core_models.Employee.objects.filter(
                    user__email=emp.get('company_email')
                ).exists():
                    date_format = '%B %d, %Y'

                    new_employee = core_models.Employee(
                        client=client,
                        user=self.create_user(
                            first_name=emp.get('first_name'),
                            last_name=emp.get('last_name'),
                            middle_name=emp.get('middle_name'),
                            email=emp.get('company_email')
                        )[0],
                        employee_id=emp.get('employee_id'),
                        gender=int(emp.get('gender')),
                        date_hired=datetime.strptime(
                            emp.get('date_hired'), date_format
                        ),
                        job_title=self.get_jobtitle(
                            client=client,
                            name=emp.get('job_title')
                        ),
                        address_1=emp.get('address_1'),
                        address_2=emp.get('address_2'),
                        mobile_number=emp.get('mobile_number'),
                        martial_status=int(emp.get('martial_status')),
                        birthday=datetime.strptime(
                            emp.get('birthday'), date_format
                        ),
                        employee_status=int(emp.get('employee_status')),
                        office_location=self.get_off_location(
                            client=client,
                            name=emp.get('office_location')
                        ),
                        level=self.get_level(
                            client=client,
                            name=emp.get('level')
                        ),
                        work_arrangement=int(emp.get('work_arrangement')),
                        department=self.get_department(
                            client=client,
                            name=emp.get('department')
                        ),
                        cpioe=emp.get('pioe'),
                        cpioe_contact_no=emp.get('cpioe_contact_no'),
                    )
                    new_employee.save()
                else:
                    self.stdout.write(self.style.WARNING(
                        "Employee %s %s already exists." % (
                            emp.get('first_name'), emp.get('last_name')
                        ))
                    )

        self.stdout.write(self.style.SUCCESS(
            'Successfully upload data')
        )
