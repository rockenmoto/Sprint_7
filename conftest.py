import pytest

from courier import Courier


@pytest.fixture(scope='function')
def courier():
    cr = Courier()
    return cr


@pytest.fixture(scope='function')
def courier_data(request, courier):
    yield courier.register_new_courier_and_return_login_password()

    login = courier.register_new_courier_and_return_login_password()[0]
    password = courier.register_new_courier_and_return_login_password()[1]
    courier.delete_courier(login, password)
