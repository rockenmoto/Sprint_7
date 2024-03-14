import allure
import pytest
import requests


class TestCreateCourier:
    login_already_use_error_text = 'Этот логин уже используется. Попробуйте другой.'
    not_enough_data_error_text = 'Недостаточно данных для создания учетной записи'

    @allure.title('Проверяем успешное создание курьера c обязательными полями')
    def test_create_courier_with_required_fields_true(self, courier, courier_data):
        assert len(courier_data) == 3

    @allure.title('Проверяем создание 2 курьеров с одинаковыми данными')
    def test_create_two_same_couriers_false(self, courier, courier_data):
        login = courier_data[0]
        password = courier_data[1]
        first_name = courier_data[2]

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(courier.base_courier_url, data=payload)
        assert (response.json()['code'] == 409 and
                response.json()['message'] == self.login_already_use_error_text)

    @allure.title('Проверяем создание курьера с одинаковым логином')
    def test_create_courier_with_same_login_false(self, courier, courier_data):
        login = courier_data[0]
        password = courier.generate_random_string(10)
        first_name = courier.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(courier.base_courier_url, data=payload)
        assert (response.json()['code'] == 409 and
                response.json()['message'] == self.login_already_use_error_text)

    @allure.title('Проверяем код и текст успешного ответа')
    def test_create_courier_status_code_and_text_true(self, courier, courier_data):
        assert (courier.response.status_code == 201 and courier.response.json() == {'ok': True})

    @allure.title('Проверка создания курьера без обязательного поля')
    @pytest.mark.parametrize("field_one, field_two",
                             [["login", "firstName"],
                              ["password", "firstName"]
                              ])
    def test_create_courier_without_required_false(self, courier, field_one, field_two):
        field_one_data = courier.generate_random_string(10)
        field_two_data = courier.generate_random_string(10)

        payload = {
            f"{field_one}": field_one_data,
            f"{field_two}": field_two_data
        }

        response = requests.post(courier.base_courier_url, data=payload)
        assert (response.status_code == 400 and
                response.json()['message'] == self.not_enough_data_error_text)
