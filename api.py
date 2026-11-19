import time
import allure
import requests
from requests.exceptions import RequestException
from routes import Routes
from settings import REQUEST_TIMEOUT


RETRY_COUNT = 3
RETRY_DELAY_SECONDS = 2

def _request_with_retry(method, url, **kwargs):
    """
    Отправляет HTTP-запрос с повтором при сетевых ошибках и таймаутах.
    """
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)

    last_exception = None

    for attempt in range(RETRY_COUNT):
        try:
            return method(url, **kwargs)
        except RequestException as exc:
            last_exception = exc

            if attempt < RETRY_COUNT - 1:
                time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))

    raise last_exception


@allure.step("Создание курьера")
def create_courier(payload):
    # Отправляет запрос на создание курьера
    return _request_with_retry(
        requests.post,
        Routes.COURIER_CREATE,
        json=payload,
    )


@allure.step("Логин курьера")
def login_courier(payload):
    # Отправляет запрос на логин курьера
    return _request_with_retry(
        requests.post,
        Routes.COURIER_LOGIN,
        json=payload,
    )


@allure.step("Создание заказа")
def create_order(payload):
    # Отправляет запрос на создание заказа
    return _request_with_retry(
        requests.post,
        Routes.ORDER_CREATE,
        json=payload,
    )


@allure.step("Получение списка заказов")
def get_orders_list(params=None):
    # Отправляет запрос на получение списка заказов
    return _request_with_retry(
        requests.get,
        Routes.ORDER_LIST,
        params=params,
    )


@allure.step("Служебное удаление курьера")
def delete_courier(courier_id):
    # Служебный запрос на удаление курьера
    return _request_with_retry(
        requests.delete,
        f"{Routes.COURIER_CREATE}/{courier_id}",
    )


@allure.step("Служебная отмена заказа")
def cancel_order(track):
    # Служебный запрос на отмену заказа
    return _request_with_retry(
        requests.put,
        f"{Routes.ORDER_CREATE}/cancel",
        params={"track": track},
    )
