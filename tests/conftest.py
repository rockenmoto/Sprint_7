import pytest

from courier import Courier


@pytest.fixture(scope='function')
def courier():
    cr = Courier()
    return cr


@pytest.fixture(scope='function')
def courier_data(courier):
    cr_data = courier.register_new_courier_and_return_login_password()
    login = cr_data[0]
    password = cr_data[1]
    yield cr_data

    courier.delete_courier(login, password)
