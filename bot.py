import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from third_party import generate_random_code
from models import Order

session = None  # sends messages
host = None  # gets messages
answer_settings = {'out': 0, 'count': 1, 'time_offset': 300}
to_client_answers = ['Здравствуйте, представьтесь, пожалуйста!', 'Хорошо, выберите тариф', 'Откуда вас забрать?',
                     'Куда вам нужно?', 'Спасибо, ожидайте, пока кто-нибудь из водителей примет ваш заказ!']
to_driver_answers = ['Введите логин:', 'Введите пароль:']
active_orders = list()
active_drivers = list()


def init():
    global session, host
    session = vk_api.VkApi(token='YOUR_TOKEN')
    host = VkLongPoll(session)
    main_loop()


def send_message(user_id, message):
    session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': generate_random_code()})


def main_loop():
    """
        this loop receives client answers

        'user_doing_order' is a dictionary with key of user_id and a value of message
        that will be sent to the user after he answers + user credentials
    """
    users_doing_order = dict(dict())
    authenticating_drivers = dict(dict())
    for event in host.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.text == 'Вызвать такси' and not (event.user_id in authenticating_drivers.keys()):
                    users_doing_order[event.user_id] = {
                        'order_step': 0,
                        'name': '',
                        'address_from': '',
                        'address_to': '',
                        'class_auto': '',
                    }
                    send_message(event.user_id, to_client_answers[0])
                    users_doing_order[event.user_id]['order_step'] += 1
                elif event.text == 'Аутентификация водителя':
                    authenticating_drivers[event.user_id] = {
                        'auth_step': 0,
                        'login': '',
                        'password': '',
                    }
                    send_message(event.user_id, to_driver_answers[0])
                    authenticating_drivers[event.user_id]['auth_step'] += 1
                elif event.user_id in users_doing_order.keys():
                    step = users_doing_order[event.user_id]['order_step']
                    # setting name
                    if step == 1:
                        users_doing_order[event.user_id]['name'] = event.text
                        send_message(event.user_id, to_client_answers[step])
                        users_doing_order[event.user_id]['order_step'] += 1
                    # setting tariff
                    if step == 2:
                        users_doing_order[event.user_id]['class_auto'] = event.text
                        send_message(event.user_id, to_client_answers[step])
                        users_doing_order[event.user_id]['order_step'] += 1
                    # setting address_from
                    if step == 3:
                        users_doing_order[event.user_id]['address_from'] = event.text
                        send_message(event.user_id, to_client_answers[step])
                        users_doing_order[event.user_id]['order_step'] += 1
                    # setting address_to
                    if step == 4:
                        users_doing_order[event.user_id]['address_to'] = event.text
                        send_message(event.user_id, to_client_answers[step])
                        active_orders.append(Order(event.user_id, users_doing_order[event.user_id]))
                        del users_doing_order[event.user_id]
                elif event.user_id in authenticating_drivers.keys():
                    step = authenticating_drivers[event.user_id]['auth_step']
                    # login
                    if step == 1:
                        authenticating_drivers[event.user_id]['login'] = event.text
                        send_message(event.user_id, to_driver_answers[step])
                        authenticating_drivers[event.user_id]['auth_step'] += 1
                    # password
                    if step == 2:
                        authenticating_drivers[event.user_id]['password'] = event.text
                        # firebase database
                        del authenticating_drivers[event.user_id]
                else:
                    send_message(event.user_id,
                                 'Простите, мы не понимаем вас. Чтобы вызвать такси, введите "Вызвать такси"')
