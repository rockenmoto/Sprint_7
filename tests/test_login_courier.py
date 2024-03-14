import allure
import requests


class TestLoginCourier:
    account_not_found_error_text = 'Учетная запись не найдена'
    insufficient_data_error_text = 'Недостаточно данных для входа'

    @allure.title('Проверка авторизация курьера с обязательными полями')
    def test_login_courier_true(self, courier, courier_data):
        login = courier_data[0]
        password = courier_data[1]

        payload = {
            "login": f"{login}",
            "password": f"{password}"
        }

        response = requests.post(f'{courier.base_courier_url}login',
                                 data=payload)
        assert response.status_code == 200 and response.json()["id"] != ''

    @allure.title('Проверка авторизация с неверным логином или паролем')
    def test_login_courier_with_incorrect_data_false(self, courier, courier_data):
        fake_login = "fake_login"
        fake_pas = "fake_password"

        payloads = [{"login": f"{courier_data[0]}", "password": fake_pas},
                    {"login": fake_login, "password": f"{courier_data[1]}"}]

        for payload in payloads:
            response = requests.post(f'{courier.base_courier_url}login',
                                     data=payload)
            assert response.status_code == 404 and response.json()['message'] == self.account_not_found_error_text

    @allure.title('Проверка авторизация с пустым логином или паролем')
    def test_login_courier_with_empty_data_false(self, courier, courier_data):
        payloads = [{"login": f"{courier_data[0]}", "password": ""},
                    {"login": "", "password": f"{courier_data[1]}"}]

        for payload in payloads:
            response = requests.post(f'{courier.base_courier_url}login',
                                     data=payload)
            assert response.status_code == 400 and response.json()['message'] == self.insufficient_data_error_text
