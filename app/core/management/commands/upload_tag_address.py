from django.core.management.base import BaseCommand
from core import models as core_models
from client import core as client_core
from django.db import transaction
import json


class Command(
    BaseCommand,
    client_core.Core
):

    help = "Upload outlet data"

    def upload_regions(self, *args, **option):
        core_models.Region.objects.bulk_create(
            [
                core_models.Region(
                    name=reg.get("name"),
                )
                for reg in json.loads(open(
                    'core/management/json/regions.json'
                ).read())
            ]
        )

        self.stdout.write(self.style.SUCCESS(
            'Successfully Region data')
        )

    def upload_province(self, *args, **option):
        core_models.Province.objects.bulk_create(
            [
                core_models.Province(
                    name=pro.get("name"),
                    region=self.get_region(
                        id=pro.get('region')
                    ).first()
                )
                for pro in json.loads(open(
                    'core/management/json/provinces.json'
                ).read())
            ]
        )

        self.stdout.write(self.style.SUCCESS(
            'Successfully Provice data')
        )

    def upload_city(self, *args, **option):
        core_models.City.objects.bulk_create(
            [
                core_models.City(
                    province=self.get_province(
                        id=cty.get('province')
                    ).first(),
                    name=cty.get("name"),
                )
                for cty in json.loads(open(
                    'core/management/json/municipalities.json'
                ).read())
            ]
        )

        self.stdout.write(self.style.SUCCESS(
            'Successfully City data')
        )

    def upload_brangay(self, *args, **option):
        core_models.Barangay.objects.bulk_create(
            [
                core_models.Barangay(
                    city=self.get_city(
                        id=brgy.get('city')
                    ).first(),
                    name=brgy.get("name"),
                )
                for brgy in json.loads(open(
                    'core/management/json/barangays.json'
                ).read())
            ]
        )

        self.stdout.write(self.style.SUCCESS(
            'Successfully Barangay data')
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            self.upload_regions()
            self.upload_province()
            self.upload_city()
            self.upload_brangay()
