class Order:
    def __init__(self, user_id, order_credentials: dict):
        self.user_id = user_id
        self.name = order_credentials['name']
        self.address_from = order_credentials['address_from']
        self.address_to = order_credentials['address_to']
        self.class_auto = order_credentials['class_auto']

    def to_string(self):
        text = str()
        text += 'Имя: ' + self.name + '\n'
        text += 'Тариф: ' + self.class_auto + '\n'
        text += 'Откуда: ' + self.address_from + '\n'
        text += 'Куда: ' + self.address_to + '\n'
        return text


class DriverLogIn:
    def __init__(self, user_id, driver_credentials: dict):
        self.user_id = user_id
        self.login = driver_credentials['login']
        self.password = driver_credentials['password']
