import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from helpers import generate_random_string, login_courier

class TestCourierLogin:
    
    @allure.title("Успешный логин курьера")
    @allure.step("Тест успешного логина курьера")
    def test_login_courier_success(self, courier):
        response = login_courier(courier["login"], courier["password"])
        assert response.status_code == 200, "Ожидался успешный логин"
        assert "id" in response.json(), "В ответе должен быть id курьера"
        assert isinstance(response.json()["id"], int), "ID должен быть числом"
    
    @allure.title("Логин без логина")
    @allure.step("Тест логина без логина")
    def test_login_missing_login(self):
        response = login_courier("", generate_random_string(10))
        assert response.status_code == 400, f"Ожидалась ошибка 400, получено: {response.status_code}"
        assert "message" in response.json(), "В ответе должно быть сообщение об ошибке"
        assert response.json()["message"] == "Недостаточно данных для входа"
    
    @allure.title("Логин с неверным паролем")
    @allure.step("Тест логина с неверным паролем")
    def test_login_wrong_password(self, courier):
        wrong_password = courier["password"] + "_wrong"
        response = login_courier(courier["login"], wrong_password)
        assert response.status_code == 404, "Ожидалась ошибка 404 при неверном пароле"
        assert "message" in response.json(), "В ответе должно быть сообщение об ошибке"
        assert response.json()["message"] == "Учетная запись не найдена"
    
    @allure.title("Логин с неверным логином")
    @allure.step("Тест логина с неверным логином")
    def test_login_wrong_login(self, courier):
        wrong_login = courier["login"] + "_wrong"
        response = login_courier(wrong_login, courier["password"])
        assert response.status_code == 404, "Ожидалась ошибка 404 при неверном логине"
        assert "message" in response.json(), "В ответе должно быть сообщение об ошибке"
        assert response.json()["message"] == "Учетная запись не найдена"
    
    @allure.title("Логин несуществующего курьера")
    @allure.step("Тест логина несуществующего курьера")
    def test_login_nonexistent_courier(self):
        response = login_courier("nonexistent_login", "nonexistent_password")
        assert response.status_code == 404, "Ожидалась ошибка 404 для несуществующего курьера"
        assert "message" in response.json(), "В ответе должно быть сообщение об ошибке"
        assert response.json()["message"] == "Учетная запись не найдена"
    
    @allure.title("Логин без логина (обязательное поле)")
    @allure.step("Тест логина без логина (обязательное поле)")
    def test_login_missing_login_required(self, courier):
        response = login_courier("", courier["password"])
        assert response.status_code == 400, f"Ожидалась ошибка 400 без логина, получено: {response.status_code}"
        assert "message" in response.json(), "В ответе должно быть сообщение об ошибке"
        assert response.json()["message"] == "Недостаточно данных для входа"
    
    @allure.title("Логин без пароля (обязательное поле)")
    @allure.step("Тест логина без пароля (обязательное поле)")
    def test_login_missing_password_required(self, courier):
        response = login_courier(courier["login"], "")
        assert response.status_code == 400, f"Ожидалась ошибка 400 без пароля, получено: {response.status_code}"
        assert "message" in response.json(), "В ответе должно быть сообщение об ошибке"
        assert response.json()["message"] == "Недостаточно данных для входа"