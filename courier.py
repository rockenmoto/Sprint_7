import string
import random
import allure

import requests


class Courier:
    base_courier_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/'

    @allure.step('Регистрация нового курьера с возвращением списка из логина и пароля')
    def register_new_courier_and_return_login_password(self):
        # создаём список, чтобы метод мог его вернуть
        login_pass = []

        # генерируем логин, пароль и имя курьера
        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post(self.base_courier_url, data=payload)

        # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)

        # возвращаем список
        return login_pass

    @allure.step('Удаление курьера')
    def delete_courier(self, login, password):
        courier_id = self.get_courier_id(login, password)
        payload_del = {"id": f"{courier_id}"}
        requests.delete(f'{self.base_courier_url}{courier_id}',
                        data=payload_del)

    @allure.step('Получение id курьера')
    def get_courier_id(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{self.base_courier_url}login',
                                 data=payload)
        return response.json()['id']

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
