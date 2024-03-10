import allure
import pytest
import requests


class TestLoginCourier:
    @allure.step('Проверка авторизация курьера с обязательными полями')
    def test_login_courier_true(self, courier, register_new_courier_and_return_login_password):
        login = register_new_courier_and_return_login_password[0]
        password = register_new_courier_and_return_login_password[1]

        payload = {
            "login": f"{login}",
            "password": f"{password}"
        }

        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data=payload)
        assert response.status_code == 200 and response.json()["id"] != ''
        courier.delete_courier(login, password)

    @allure.step('Проверка авторизация с неверным логином или паролем')
    def test_login_courier_with_incorrect_data_false(self, register_new_courier_and_return_login_password):
        fake_login = "fake_login"
        fake_pas = "fake_password"

        payloads = [{"login": f"{register_new_courier_and_return_login_password[0]}", "password": fake_pas},
                    {"login": fake_login, "password": f"{register_new_courier_and_return_login_password[1]}"}]

        for payload in payloads:
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                     data=payload)
            assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.step('Проверка авторизация с пустым логином или паролем')
    def test_login_courier_with_empty_data_false(self, register_new_courier_and_return_login_password):
        payloads = [{"login": f"{register_new_courier_and_return_login_password[0]}", "password": ""},
                    {"login": "", "password": f"{register_new_courier_and_return_login_password[1]}"}]

        for payload in payloads:
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                     data=payload)
            assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа'
