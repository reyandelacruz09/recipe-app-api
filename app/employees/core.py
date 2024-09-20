from core import models as core_models


class Core():

    @classmethod
    def save_employee(cls, user, client, **kwargs):
        return core_models.Employee(
            user=user,
            client=client,
            **kwargs
        ).save()

    @classmethod
    def edit_employee(cls, id, **kwargs):
        emp = core_models.Employee.objects.filter(
            id=id
        )

        return emp(**kwargs).save()

    @classmethod
    def get_emp(cls, **kwargs):
        return core_models.Employee.objects.filter(
            **kwargs
        )

    @classmethod
    def save_educ_back(cls, emp, **kwargs):
        return core_models.EducBackGround(
            employee=emp,
            **kwargs
        ).save()

    @classmethod
    def save_emp_benefits(cls, benefits, employee, **kwargs):
        return core_models.EmployeeBenefits(
            benefits=benefits,
            employee=employee,
            **kwargs
        ).save()

    @classmethod
    def emp_benefits(cls, **kwargs):
        return core_models.EmployeeBenefits.objects.filter(
            **kwargs
        )

    @classmethod
    def save_emp_compensation(cls, employee, compensation, **kwargs):
        return core_models.EmployeeCompensation(
            employee=employee,
            compensation=compensation,
            **kwargs
        ).save()

    @classmethod
    def emp_compensation(cls, **kwargs):
        return core_models.EmployeeCompensation.objects.filter(
            **kwargs
        )
