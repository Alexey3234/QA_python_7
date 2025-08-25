import requests
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from helpers import generate_random_string, login_courier, delete_courier
from urls import Urls

class TestCourierCreation:
    
    @allure.title("Успешное создание курьера")
    @allure.step("Создание курьера с валидными данными")
    def test_create_courier_success(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_response = login_courier(payload["login"], payload["password"])
        assert login_response.status_code == 200
        assert "id" in login_response.json()
        
        courier_id = login_response.json()["id"]
        delete_courier(courier_id)
    
    @allure.title("Создание дубликата курьера")
    @allure.step("Попытка создания курьера с уже существующим логином")
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
    def test_create_courier_missing_login(self):
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        
        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}
    
    @allure.title("Создание курьера без пароля")
    @allure.step("Попытка создания курьера без указания пароля")
    def test_create_courier_missing_password(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        
        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}
    
    @allure.title("Создание курьера без имени")
    @allure.step("Создание курьера без указания имени (необязательное поле)")
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
        
        courier_id = login_response.json()["id"]
        delete_courier(courier_id)
    
    @allure.title("Создание курьера со всеми полями")
    @allure.step("Создание курьера с указанием всех полей")
    def test_create_courier_with_all_fields(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_response = login_courier(payload["login"], payload["password"])
        assert login_response.status_code == 200
        assert "id" in login_response.json()
        
        courier_id = login_response.json()["id"]
        delete_courier(courier_id)

    @allure.title("Создание курьера с пустым логином")
    @allure.step("Попытка создания курьера с пустым логином")
    def test_create_courier_empty_login(self):
        payload = {
            "login": "",
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        
        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}

    @allure.title("Создание курьера с пустым паролем")
    @allure.step("Попытка создания курьера с пустым паролем")
    def test_create_courier_empty_password(self):
        payload = {
            "login": generate_random_string(10),
            "password": "",
            "firstName": generate_random_string(10)
        }
        
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        
        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}