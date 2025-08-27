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
        
        order_data["color"] = color
        
        response = create_order(order_data)
        
        assert response.status_code == 201, f"Не удалось создать заказ для {description}"
        
        response_data = response.json()
        assert "track" in response_data, f"Отсутствует track в ответе для {description}"
        
        track_number = response_data["track"]
        cleanup_order.append(track_number)
    
    @allure.title("Проверка тела ответа при создании заказа")
    @allure.step("Тест тела ответа при создании заказа")
    def test_order_response_body(self, cleanup_order):
        order_data = BASE_ORDER_DATA.copy()
        
        response = create_order(order_data)
        
        assert response.status_code == 201
        
        response_body = response.json()
        assert "track" in response_body
        assert isinstance(response_body["track"], int)
        assert response_body["track"] > 0
        
        cleanup_order.append(response_body["track"])