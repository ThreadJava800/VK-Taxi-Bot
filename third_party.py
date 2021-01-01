from random import choice
from string import digits
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from models import Driver


def generate_random_code():
    code = list()
    for i in range(6):
        code.append(choice(digits))
    return ''.join(code)


def __init_firebase__():
    cred = credentials.Certificate('YOUR_PATH_TO_FILE')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'YOUR_DB_URL'
    })


def auth_driver(user_id, login, password):
    __init_firebase__()
    snapshot = db.reference('drivers').get()
    for driver in snapshot:
        driver_credentials = snapshot[driver]
        if driver_credentials['login'] == login and driver_credentials['password'] == password:
            driver_reference = db.reference('drivers').child(driver)
            # driver is online
            driver_reference.update({
                'active': 1,
            })
            return Driver(user_id, driver_credentials)
    return None
