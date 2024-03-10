import string
import random

import requests


class Courier:
    login = ''
    password = ''
    first_name = ''

    # метод регистрации нового курьера возвращает список из логина и пароля
    # если регистрация не удалась, возвращает пустой список
    def register_new_courier_and_return_login_password(self):
        # создаём список, чтобы метод мог его вернуть
        login_pass = []

        # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
        if self.create_courier().status_code == 201:
            login_pass.append(self.login)
            login_pass.append(self.password)
            login_pass.append(self.first_name)

        # возвращаем список
        return login_pass

    def create_courier(self):
        self.login = self.generate_random_string(10)
        self.password = self.generate_random_string(10)
        self.first_name = self.generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": self.login,
            "password": self.password,
            "firstName": self.first_name
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        return response

    def delete_courier(self, login, password):
        courier_id = self.get_courier_id(login, password)
        payload_del = {
            "id": f"{courier_id}"
        }

        return requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}',
                               data=payload_del)

    def get_courier_id(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                                 data=payload)
        return response.json()['id']

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
