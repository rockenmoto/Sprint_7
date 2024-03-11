import allure
import requests

from courier import Courier


class TestLoginCourier:
    @allure.step('Проверка авторизация курьера с обязательными полями')
    def test_login_courier_true(self):
        courier = Courier()
        courier_data = courier.register_new_courier_and_return_login_password()

        login = courier_data[0]
        password = courier_data[1]

        payload = {
            "login": f"{login}",
            "password": f"{password}"
        }

        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data=payload)
        assert response.status_code == 200 and response.json()["id"] != ''
        courier.delete_courier(login, password)

    @allure.step('Проверка авторизация с неверным логином или паролем')
    def test_login_courier_with_incorrect_data_false(self):
        courier = Courier()
        courier_data = courier.register_new_courier_and_return_login_password()

        fake_login = "fake_login"
        fake_pas = "fake_password"

        payloads = [{"login": f"{courier_data[0]}", "password": fake_pas},
                    {"login": fake_login, "password": f"{courier_data[1]}"}]

        for payload in payloads:
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                     data=payload)
            assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.step('Проверка авторизация с пустым логином или паролем')
    def test_login_courier_with_empty_data_false(self):
        courier = Courier()
        courier_data = courier.register_new_courier_and_return_login_password()

        payloads = [{"login": f"{courier_data[0]}", "password": ""},
                    {"login": "", "password": f"{courier_data[1]}"}]

        for payload in payloads:
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                     data=payload)
            assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа'
