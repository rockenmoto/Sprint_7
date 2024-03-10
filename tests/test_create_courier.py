import allure
import pytest
import requests


class TestCreateCourier:
    @allure.step('Проверяем успешное создание курьера c обязательными полями')
    def test_create_courier_with_required_fields_true(self, courier, register_new_courier_and_return_login_password):
        login = register_new_courier_and_return_login_password[0]
        password = register_new_courier_and_return_login_password[1]
        assert len(register_new_courier_and_return_login_password) == 3
        courier.delete_courier(login, password)

    @allure.step('Проверяем создание 2 курьеров с одинаковыми данными')
    def test_create_two_same_couriers_false(self, courier, register_new_courier_and_return_login_password):
        login = register_new_courier_and_return_login_password[0]
        password = register_new_courier_and_return_login_password[1]
        first_name = register_new_courier_and_return_login_password[2]

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert (response.json()['code'] == 409 and
                response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.')
        courier.delete_courier(login, password)

    @allure.step('Проверяем создание курьера с одинаковым логином')
    def test_create_courier_with_same_login_false(self, courier, register_new_courier_and_return_login_password):
        login = register_new_courier_and_return_login_password[0]
        password = courier.generate_random_string(10)
        first_name = courier.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert (response.json()['code'] == 409 and
                response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.')
        old_password = register_new_courier_and_return_login_password[1]
        courier.delete_courier(login, old_password)

    @allure.step('Проверяем код и текст успешного ответа')
    def test_create_courier_status_code_and_text_true(self, courier):
        login = courier.generate_random_string(10)
        password = courier.generate_random_string(10)
        first_name = courier.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert (response.status_code == 201 and response.json() == {'ok': True})
        courier.delete_courier(login, password)

    @allure.step('Проверка создания курьера без обязательного поля')
    @pytest.mark.parametrize("field_one, field_two",
                             [["login", "firstName"],
                              ["password", "firstName"]
                              ])
    def test_create_courier_status_code_and_text_true(self, courier, field_one, field_two):
        field_one_data = courier.generate_random_string(10)
        field_two_data = courier.generate_random_string(10)

        payload = {
            f"{field_one}": field_one_data,
            f"{field_two}": field_two_data
        }

        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert (response.status_code == 400 and
                response.json()['message'] == ('Недостаточно данных для создания учетной записи'))
