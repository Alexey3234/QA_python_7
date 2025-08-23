import requests
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from helpers import generate_random_string
from urls import Urls

class TestCourierCreation:
    
    @allure.title("Успешное создание курьера через фикстуру")
    @allure.step("Тест успешного создания курьера через фикстуру")
    def test_create_courier_success(self, courier):
        assert isinstance(courier["id"], int)
        assert courier["id"] > 0
        assert isinstance(courier["login"], str)
        assert len(courier["login"]) > 0
        assert isinstance(courier["password"], str)
        assert len(courier["password"]) > 0
    
    @allure.title("Создание дубликата курьера")
    @allure.step("Тест создания двух одинаковых курьеров")
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
    @allure.step("Тест создания курьера без логина")
    def test_create_courier_missing_login(self, courier_payload_missing_login):
        response = requests.post(Urls.CREATE_COURIER, data=courier_payload_missing_login)
        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}
    
    @allure.title("Создание курьера без пароля")
    @allure.step("Тест создания курьера без пароля")
    def test_create_courier_missing_password(self, courier_payload_missing_password):
        response = requests.post(Urls.CREATE_COURIER, data=courier_payload_missing_password)
        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}

    @allure.title("Создание курьера без имени")
    @allure.step("Тест создания курьера без имени")
    def test_create_courier_without_first_name(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
        
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_resp = requests.post(Urls.LOGIN_COURIER, data={
            "login": payload["login"],
            "password": payload["password"]
        })
        if login_resp.status_code == 200:
            courier_id = login_resp.json()["id"]
            requests.delete(f"{Urls.DELETE_COURIER}{courier_id}")

    @allure.title("Создание курьера без логина (обязательное поле)")
    @allure.step("Тест создания курьера без логина (обязательное поле)")
    def test_create_courier_missing_login_required(self):
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}

    @allure.title("Создание курьера без пароля (обязательное поле)")
    @allure.step("Тест создания курьера без пароля (обязательное поле)")
    def test_create_courier_missing_password_required(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}
    
    @allure.title("Создание курьера со всеми полями")
    @allure.step("Тест создания курьера со всеми полями")
    def test_create_courier_with_all_fields(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_resp = requests.post(Urls.LOGIN_COURIER, data={
            "login": payload["login"],
            "password": payload["password"]
        })
        if login_resp.status_code == 200:
            courier_id = login_resp.json()["id"]
            requests.delete(f"{Urls.DELETE_COURIER}{courier_id}")