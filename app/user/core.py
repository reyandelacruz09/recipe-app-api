from core import models as core_models


class Core():

    @classmethod
    def user_get(cls, id):
        return core_models.User.objects.filter(
            id=id
        ).first()

    @classmethod
    def create_user(cls, **kwargs):
        u_password = cls.generate_int_str(9)
        print('Email: ' + kwargs['email'])
        print('Password: ' + u_password)
        user = core_models.User(
            **kwargs
        )
        user.set_password(u_password)
        user.save()
        return user, u_password
