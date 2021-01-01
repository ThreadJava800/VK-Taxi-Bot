from random import choice
from string import digits


def generate_random_code():
    code = list()
    for i in range(6):
        code.append(choice(digits))
    return ''.join(code)


def find_driver(login, password):
    pass
