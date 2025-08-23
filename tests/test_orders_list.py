import pytest
import requests
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from helpers import get_orders_list
from urls import Urls

class TestOrdersList:
    
    @allure.title("Получение списка заказов")
    @allure.step("Тест получения списка заказов")
    def test_get_orders_list(self):
        response = get_orders_list()
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        
        content_type = response.headers.get('Content-Type', '')
        assert 'application/json' in content_type, f"Ответ должен быть в формате JSON, получен: {content_type}"
        
        response_json = response.json()
        assert "orders" in response_json, "В ответе должно быть поле 'orders'"
        assert isinstance(response_json["orders"], list), "Поле 'orders' должно быть списком"
        
        if response_json["orders"]:
            first_order = response_json["orders"][0]
            assert "id" in first_order, "Заказ должен содержать поле 'id'"
            assert "track" in first_order, "Заказ должен содержать поле 'track'"
            assert "firstName" in first_order, "Заказ должен содержать поле 'firstName'"
            assert "lastName" in first_order, "Заказ должен содержать поле 'lastName'"
            assert "address" in first_order, "Заказ должен содержать поле 'address'"
            assert "metroStation" in first_order, "Заказ должен содержать поле 'metroStation'"
            assert "phone" in first_order, "Заказ должен содержать поле 'phone'"
            assert "rentTime" in first_order, "Заказ должен содержать поле 'rentTime'"
            assert "deliveryDate" in first_order, "Заказ должен содержать поле 'deliveryDate'"
            assert "status" in first_order, "Заказ должен содержать поле 'status'"
            
            assert isinstance(first_order["id"], int), "ID заказа должен быть числом"
            assert isinstance(first_order["track"], int), "Track номер должен быть числом"
            assert isinstance(first_order["firstName"], str), "Имя должно быть строкой"
            assert isinstance(first_order["lastName"], str), "Фамилия должна быть строкой"
        
        allure.dynamic.description(f"Получено заказов: {len(response_json['orders'])}")
    
    @allure.title("Пагинация списка заказов с лимитом {limit}")
    @allure.step("Тест пагинации списка заказов")
    @pytest.mark.parametrize("limit", [1, 5, 10, 30])
    def test_orders_list_pagination(self, limit):
        params = {"limit": limit}
        response = requests.get(Urls.GET_ORDERS_LIST, params=params)
        assert response.status_code == 200, f"Ожидался код 200 для лимита {limit}"
        
        response_json = response.json()
        assert "orders" in response_json, "В ответе должно быть поле 'orders'"
        assert isinstance(response_json["orders"], list), "Поле 'orders' должно быть списком"
        assert len(response_json["orders"]) <= limit, f"Количество заказов превышает лимит {limit}"
    
    @allure.title("Получение списка заказов с лимитом")
    @allure.step("Тест получения списка заказов с лимитом")
    def test_orders_list_with_limit(self):
        params = {"limit": 5}
        response = requests.get(Urls.GET_ORDERS_LIST, params=params)
        assert response.status_code == 200
        
        response_json = response.json()
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)
        assert len(response_json["orders"]) <= 5
    
    @allure.title("Получение списка заказов с номером страницы")
    @allure.step("Тест получения списка заказов с номером страницы")
    def test_orders_list_with_page(self):
        params = {"page": 1}
        response = requests.get(Urls.GET_ORDERS_LIST, params=params)
        assert response.status_code == 200
        
        response_json = response.json()
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)
    
    @allure.title("Получение списка заказов с комбинированными параметрами")
    @allure.step("Тест получения списка заказов с комбинированными параметрами")
    def test_orders_list_with_combined_params(self):
        params = {"limit": 3, "page": 2}
        response = requests.get(Urls.GET_ORDERS_LIST, params=params)
        assert response.status_code == 200
        
        response_json = response.json()
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)
        assert len(response_json["orders"]) <= 3