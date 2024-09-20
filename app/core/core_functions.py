from core import models as core_models
from itertools import count
import string
import random


class Core():

    @classmethod
    def generate_string(cls, length):
        return ''.join(
            random.choice(string.ascii_letters) for x in range(length))

    @classmethod
    def generate_integer(cls, length):
        return ''.join(random.choice(string.digits) for x in range(length))

    @classmethod
    def generate_int_str(cls, length):
        return ''.join(random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(length))

    @classmethod
    def sending_notification(cls, **kwargs):
        print(kwargs)

        notification = core_models.Notification(
            **kwargs
        )
        notification.save()

        return 'notification'

    @classmethod
    def gen_cntrl_num(cls, type):
        value = 100000
        for i in count(value):
            transaction_id = str(i)
            if type == 1:
                transaction_number = f'CN-{transaction_id}'
                if not core_models.Document.objects.filter(
                    control_number=transaction_number
                ).exists():
                    return transaction_number
            if type == 2:
                transaction_number = f'MEMO-{transaction_id}'
                if not core_models.News.objects.filter(
                    memo_number=transaction_number
                ).exists():
                    return transaction_number
