import allure
import pytest
from data import COLOR_BLACK, COLOR_GREY
from expected import Expected


@allure.epic("API учебного сервиса Яндекс Самокат")
@allure.feature("Заказы")
class TestCreateOrder:

    @allure.story("Создание заказа с разными вариантами цвета")
    @allure.title("Создание заказа с разными вариантами цвета")
    @allure.description(
        "Создаём заказ с разными вариантами цвета: без цвета, только BLACK, "
        "только GREY, оба цвета. Проверяем, что сервер возвращает HTTP-статус 201 "
        "и поле track типа int."
    )
    @pytest.mark.parametrize(
        "created_order_response",
        [
            None,
            [COLOR_BLACK],
            [COLOR_GREY],
            [COLOR_BLACK, COLOR_GREY],
        ],
        indirect=True,
        ids=[
            "without_color",
            "black_only",
            "grey_only",
            "black_and_grey",
        ],
    )
    def test_create_order_color_options(self, created_order_response):
        allure.dynamic.title(
            f"Создание заказа: вариант цвета {created_order_response['color_label']}"
        )

        response = created_order_response["response"]
        body = created_order_response["body"]

        assert response.status_code == Expected.CREATED, (
            f"Ожидался статус {Expected.CREATED} при создании заказа, "
            f"но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert Expected.ORDER_CREATE_SUCCESS_TRACK_KEY in body, (
            f"В ответе отсутствует ключ '{Expected.ORDER_CREATE_SUCCESS_TRACK_KEY}'. "
            f"Тело ответа: {body}"
        )

        assert isinstance(
            body[Expected.ORDER_CREATE_SUCCESS_TRACK_KEY],
            Expected.ORDER_CREATE_SUCCESS_TRACK_TYPE,
        ), (
            f"Поле '{Expected.ORDER_CREATE_SUCCESS_TRACK_KEY}' должно быть типа "
            f"{Expected.ORDER_CREATE_SUCCESS_TRACK_TYPE.__name__}, "
            f"но получено: {type(body[Expected.ORDER_CREATE_SUCCESS_TRACK_KEY]).__name__}. "
            f"Тело ответа: {body}"
        )
        