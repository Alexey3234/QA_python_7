import requests
import random
import string
from urls import Urls
from allure import step

@step("Генерация случайной строки длиной {length}")
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

@step("Регистрация нового курьера")
def register_new_courier_and_return_login_password():
    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(Urls.CREATE_COURIER, data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass

@step("Логин курьера с логином {login}")
def login_courier(login, password):
    """Логин курьера"""
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(Urls.LOGIN_COURIER, json=payload)
    return response

@step("Получение ID курьера для логина {login}")
def get_courier_id(login, password):
    """Получение ID курьера после успешного логина"""
    response = login_courier(login, password)
    if response.status_code == 200:
        return response.json().get("id")
    return None

@step("Удаление курьера с ID {courier_id}")
def delete_courier(courier_id):
    return requests.delete(f"{Urls.DELETE_COURIER}{courier_id}")

@step("Создание заказа с данными: {order_data}")
def create_order(order_data):
    return requests.post(Urls.CREATE_ORDER, json=order_data)

@step("Получение заказа по треку {track_number}")
def get_order_by_track(track_number):
    return requests.get(f"{Urls.GET_ORDER_BY_TRACK}?t={track_number}")

@step("Получение списка заказов")
def get_orders_list():
    return requests.get(Urls.GET_ORDERS_LIST)

@step("Удаление тестового заказа с треком {track_number}")
def delete_test_order(track_number):
    try:
        return requests.delete(f"{Urls.DELETE_ORDER}{track_number}")
    except:
        return None