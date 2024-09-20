from django.core.management.base import BaseCommand
from core import models as core_models
from django.db import transaction
import json
from client import (
    department as client_dep,
    core as client_core
)


class Command(
    BaseCommand,
    client_dep.DepartmentViews,
    client_core.Core
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

            # list of Deparment instances
            department_list = [
                core_models.Department(
                    client=client,
                    name=dep.get('name'),
                )
                for dep in json.loads(open(
                    'core/management/json/department.json'
                ).read())
            ]

            core_models.Department.objects.bulk_create(
                department_list
            )

            # list of Job Title instances
            job_title_list = [
                core_models.JobTitle(
                    client=client,
                    name=job.get('name'),
                )
                for job in json.loads(open(
                    'core/management/json/jobtitle.json'
                ).read())
            ]

            core_models.JobTitle.objects.bulk_create(
                job_title_list
            )

            # list of Job Level instances
            level_list = [
                core_models.Level(
                    client=client,
                    name=lev.get('name'),
                )
                for lev in json.loads(open(
                    'core/management/json/level.json'
                ).read())
            ]

            core_models.Level.objects.bulk_create(
                level_list
            )

            # list of Office Location instances
            off_loc_list = [
                core_models.OfficeLocation(
                    client=client,
                    name=off_loc.get('name'),
                )
                for off_loc in json.loads(open(
                    'core/management/json/office_location.json'
                ).read())
            ]

            core_models.OfficeLocation.objects.bulk_create(
                off_loc_list
            )

            # list of Conpentation
            con_list = [
                core_models.ClientCompensation(
                    client=client,
                    name=con.get('name'),
                    type=int(con.get('type'))
                )
                for con in json.loads(open(
                    'core/management/json/compensation.json'
                ).read())
            ]

            core_models.ClientCompensation.objects.bulk_create(
                con_list
            )

            # list of Benefits
            benefits_list = [
                core_models.ClientBenefits(
                    client=client,
                    name=ben.get('name'),
                )
                for ben in json.loads(open(
                    'core/management/json/benefits.json'
                ).read())
            ]

            core_models.ClientBenefits.objects.bulk_create(
                benefits_list
            )

        self.stdout.write(self.style.SUCCESS(
            'Successfully upload data')
        )
