import pytest
from api import (
    create_courier,
    login_courier,
    delete_courier,
    create_order,
    cancel_order,
)
from helpers import build_courier_payload, build_order_payload, build_color_label
from expected import Expected

def _login_and_get_courier_id(login, password):

    # Служебная функция: логинит курьера и возвращает его id
    try:
        response = login_courier(
            {
                "login": login,
                "password": password,
            }
        )
    except Exception:
        return None

    if response.status_code != Expected.OK:
        return None

    try:
        body = response.json()
    except Exception:
        return None

    if not isinstance(body, dict):
        return None

    return body.get(Expected.LOGIN_SUCCESS_ID_KEY)

def _try_delete_courier(courier_id):
    # Служебная функция: пытается удалить курьера
    if courier_id is None:
        return

    try:
        delete_courier(courier_id)
    except Exception:
        pass

def _try_cancel_order(track):
    # Служебная функция: пытается отменить заказ по track
    if track is None:
        return

    try:
        cancel_order(track)
    except Exception:
        pass

@pytest.fixture
def courier_payload():
    # Фикстура: генерирует payload для создания курьера
    payload = build_courier_payload()

    yield payload

    courier_id = _login_and_get_courier_id(
        payload["login"],
        payload["password"],
    )

    _try_delete_courier(courier_id)

@pytest.fixture
def registered_courier():
    # Фикстура: создаёт курьера до теста и удаляет его после теста
    payload = build_courier_payload()

    try:
        create_response = create_courier(payload)
    except Exception as exc:
        pytest.skip(
            f"Не удалось отправить запрос на создание тестового курьера: {exc}"
        )
        return

    if create_response.status_code != Expected.CREATED:
        pytest.skip(
            f"Не удалось создать тестового курьера. "
            f"Статус: {create_response.status_code}. "
            f"Тело ответа: {create_response.text}"
        )
        return

    courier_id = _login_and_get_courier_id(
        payload["login"],
        payload["password"],
    )

    if courier_id is None:
        pytest.skip(
            "Курьер был создан, но не удалось получить его id через логин."
        )
        return

    yield {
        "login": payload["login"],
        "password": payload["password"],
        "firstName": payload["firstName"],
        "id": courier_id,
    }

    _try_delete_courier(courier_id)

@pytest.fixture
def created_order_response(request):
    # Фикстура: создаёт заказ до теста и пытается отменить его после теста
    color = request.param
    color_label = build_color_label(color)

    payload = build_order_payload(color)

    try:
        response = create_order(payload)
    except Exception as exc:
        pytest.skip(
            f"Не удалось создать тестовый заказ: {exc}"
        )
        return

    try:
        body = response.json()
    except Exception:
        body = {}

    if not isinstance(body, dict):
        body = {}

    yield {
        "response": response,
        "body": body,
        "color_label": color_label,
    }

    if response.status_code == Expected.CREATED:
        track = body.get(Expected.ORDER_CREATE_SUCCESS_TRACK_KEY)
        _try_cancel_order(track)
