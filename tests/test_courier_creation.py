import requests
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from helpers import generate_random_string, login_courier
from urls import Urls

class TestCourierCreation:

    @allure.title("Создание курьера возвращает статус 201")
    @allure.step("Отправка запроса на создание курьера")
    def test_create_courier_status_201(self, random_courier_data):
        response = requests.post(Urls.CREATE_COURIER, data=random_courier_data)
        
        assert response.status_code == 201

    @allure.title("Создание курьера возвращает 'ok: true'")
    @allure.step("Отправка запроса на создание курьера и проверка ответа")
    def test_create_courier_returns_ok_true(self, random_courier_data):
        response = requests.post(Urls.CREATE_COURIER, data=random_courier_data)
        
        assert response.json() == {"ok": True}

    @allure.title("Курьер может авторизоваться")
    @allure.step("Авторизация созданного курьера")
    def test_courier_can_login(self, courier):
        login_response = login_courier(courier["login"], courier["password"])
        
        assert login_response.status_code == 200
        assert "id" in login_response.json()

    @allure.title("Создание дубликата курьера")
    @allure.step("Попытка создания курьера с существующим логином")
    def test_create_duplicate_courier(self, courier):
        payload = {
            "login": courier["login"],
            "password": "any_password",
            "firstName": "Duplicate Name"
        }

        response = requests.post(Urls.CREATE_COURIER, data=payload)

        assert response.status_code == 409
        assert response.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}

    @allure.title("Создание курьера без логина")
    @allure.step("Попытка создания курьера без указания логина")
    def test_create_courier_missing_login(self, courier_payload_missing_login):
        response = requests.post(Urls.CREATE_COURIER, data=courier_payload_missing_login)

        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}

    @allure.title("Создание курьера без пароля")
    @allure.step("Попытка создания курьера без указания пароля")
    def test_create_courier_missing_password(self, courier_payload_missing_password):
        response = requests.post(Urls.CREATE_COURIER, data=courier_payload_missing_password)

        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}

    @allure.title("Создание курьера без имени")
    @allure.step("Создание курьера без указания имени (firstName)")
    def test_create_courier_without_first_name(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }

        response = requests.post(Urls.CREATE_COURIER, data=payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_response = login_courier(payload["login"], payload["password"])
        assert login_response.status_code == 200
        assert "id" in login_response.json()

    @allure.title("Создание курьера со всеми полями")
    @allure.step("Создание курьера с указанием всех обязательных полей")
    def test_create_courier_with_all_fields(self, random_courier_data):
        response = requests.post(Urls.CREATE_COURIER, data=random_courier_data)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_response = login_courier(random_courier_data["login"], random_courier_data["password"])
        assert login_response.status_code == 200
        assert "id" in login_response.json()