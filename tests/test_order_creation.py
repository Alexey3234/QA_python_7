# test_order_creation.py
import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from helpers import create_order
from data import BASE_ORDER_DATA, COLOR_TEST_DATA

class TestOrderCreation:
    
    @allure.title("Создание заказа с цветами: {description}")
    @pytest.mark.parametrize("color, description", COLOR_TEST_DATA, 
                           ids=[desc for _, desc in COLOR_TEST_DATA])
    @allure.step("Тест создания заказа: {description}")
    def test_create_order_with_colors(self, color, description, cleanup_order):
        order_data = BASE_ORDER_DATA.copy()
        if color:
            order_data["color"] = color
        
        response = create_order(order_data)
        assert response.status_code == 201, f"Не удалось создать заказ для {description}"
        assert "track" in response.json(), f"Отсутствует track в ответе для {description}"
        
        track_number = response.json()["track"]
        cleanup_order.append(track_number)
    
    @allure.title("Проверка тела ответа при создании заказа")
    @allure.step("Тест тела ответа при создании заказа")
    def test_order_response_body(self, cleanup_order):
        order_data = BASE_ORDER_DATA.copy()
        
        response = create_order(order_data)
        response_body = response.json()
        
        assert response.status_code == 201
        assert "track" in response_body
        assert isinstance(response_body["track"], int)
        assert response_body["track"] > 0
        
        cleanup_order.append(response_body["track"])