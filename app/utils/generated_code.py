import string
import random


class GenerateCode():

    @classmethod
    def generate_string(cls, length):
        return ''.join(random.choice(
            string.ascii_letters
        ) for x in range(length))

    @classmethod
    def generate_integer(cls, length):
        return ''.join(
            random.choice(
                string.digits
            ) for x in range(length))

    @classmethod
    def generate_int_str(cls, length):
        return ''.join(random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(length))
