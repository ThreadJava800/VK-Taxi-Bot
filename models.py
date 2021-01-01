class Order:
    def __init__(self, user_id, unique_code, order_credentials: dict):
        self.user_id = user_id
        self.name = order_credentials['name']
        self.address_from = order_credentials['address_from']
        self.address_to = order_credentials['address_to']
        self.class_auto = order_credentials['class_auto']
        self.unique_number = unique_code

    def to_string(self):
        text = str()
        text += 'Номер заказа: ' + self.unique_number + '\n'
        text += 'Имя: ' + self.name + '\n'
        text += 'Тариф: ' + self.class_auto + '\n'
        text += 'Откуда: ' + self.address_from + '\n'
        text += 'Куда: ' + self.address_to + '\n'
        return text


class Driver:
    def __init__(self, user_id, driver_credentials: dict):
        self.user_id = user_id
        self.name = driver_credentials['name']
        self.car = driver_credentials['car']
        self.car_number = driver_credentials['car_number']
        self.auto_class = driver_credentials['auto_class']
        self.location = driver_credentials['location']

    def to_string(self):
        text = str()
        text += 'Имя: ' + self.name + '\n'
        text += 'Машина: ' + self.car + '\n'
        text += 'Номер машины: ' + self.car_number + '\n'
        text += 'Класс машины: ' + self.auto_class + '\n'
        text += 'Водитель находится: ' + self.location + '\n'
        return text
