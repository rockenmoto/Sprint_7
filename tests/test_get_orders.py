import json

import allure
import requests


class TestGetOrders:
    @allure.step('Проверка получения списка всех заказов')
    def test_get_orders_list_without_courier_id_true(self):
        response = requests.get("https://qa-scooter.praktikum-services.ru/api/v1/orders")
        assert response.status_code == 200 and len(response.json()['orders']) != 0

    @allure.step('Проверка получения списка заказов без courier_id')
    def test_get_orders_list_with_incorrect_courier_id_true(self):
        fake_courier_id = 0
        response = requests.get("https://qa-scooter.praktikum-services.ru/api/v1/orders?",
                                params={'courierId': fake_courier_id})
        assert (response.status_code == 404 and
                response.json()['message'] == f'Курьер с идентификатором {fake_courier_id} не найден')

    @allure.step('Проверка получения заказа по track_id')
    def test_get_orders_list_with_incorrect_courier_id_true(self):
        track_id = 84029
        response_track = requests.get("https://qa-scooter.praktikum-services.ru/api/v1/orders/track?",
                                      params={'t': track_id})
        assert (response_track.status_code == 200 and
                len(response_track.json()['order']) != 0)
