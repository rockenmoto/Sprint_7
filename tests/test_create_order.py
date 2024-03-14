import json

import allure
import pytest
import requests


class TestCreateOrder:
    base_order_url = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

    @allure.title('Проверка создания заказа с одним или без цвета')
    @pytest.mark.parametrize("color", ["BLACK ", "GREY", ""])
    def test_create_order_with_one_and_without_color_true(self, color):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": [f"{color}"]
        }

        payload_str = json.dumps(payload)
        response = requests.post(f'{self.base_order_url}',
                                 data=payload_str)
        assert response.status_code == 201 and response.json()["track"] != ''

    @allure.title('Проверка создания заказа с двумя цветами')
    def test_create_order_with_two_colors_true(self):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": ["BLACK", "GRAY"]
        }

        payload_str = json.dumps(payload)
        response = requests.post(f'{self.base_order_url}',
                                 data=payload_str)
        assert response.status_code == 201 and response.json()["track"] != ''
