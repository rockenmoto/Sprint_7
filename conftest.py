import pytest
from courier import Courier


@pytest.fixture(scope="function")
def courier():
    courier = Courier()
    return courier


@pytest.fixture(scope="function")
def register_new_courier_and_return_login_password(courier):
    courier_data = courier.register_new_courier_and_return_login_password()
    return courier_data
