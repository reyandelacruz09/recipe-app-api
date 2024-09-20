from core import models as core_models


class Core():

    @classmethod
    def client_get(cls, id):
        return core_models.Client.objects.filter(
            id=id
        ).first()

    @classmethod
    def user_get(cls, id):
        return core_models.User.objects.filter(
            id=id
        ).first()

    @classmethod
    def get_jobtitle(cls, **kwargs):
        return core_models.JobTitle.objects.filter(
            **kwargs
        ).first()

    # This function to get the detailed by name
    @classmethod
    def get_off_location(cls, **kwargs):
        return core_models.OfficeLocation.objects.filter(
            **kwargs
        ).first()

    @classmethod
    def get_level(cls, **kwargs):
        return core_models.Level.objects.filter(
            **kwargs
        ).first()

    @classmethod
    def get_department(cls, **kwargs):
        return core_models.Department.objects.filter(
            **kwargs
        ).first()

    @classmethod
    def get_client_benefits(cls, **kwargs):
        return core_models.ClientBenefits.objects.filter(
            **kwargs
        )

    @classmethod
    def get_client_compensation(cls, **kwargs):
        return core_models.ClientCompensation.objects.filter(
            **kwargs
        )

    @classmethod
    def get_region(cls, **kwargs):
        return core_models.Region.objects.filter(
            **kwargs
        )

    @classmethod
    def get_province(cls, **kwargs):
        return core_models.Province.objects.filter(
            **kwargs
        )

    @classmethod
    def get_city(cls, **kwargs):
        return core_models.City.objects.filter(
            **kwargs
        )

    @classmethod
    def get_barangay(cls, **kwargs):
        return core_models.Barangay.objects.filter(
            **kwargs
        )
