import allure
from api import get_orders_list
from expected import Expected


@allure.epic("API учебного сервиса Яндекс Самокат")
@allure.feature("Заказы")
class TestGetOrdersList:

    @allure.story("Получение списка заказов")
    @allure.title("В ответе возвращается список заказов")
    @allure.description(
        "Отправляем запрос на получение списка заказов без дополнительных параметров. "
        "Ожидаем HTTP-статус 200, наличие поля orders и то, что orders является списком."
    )
    def test_get_orders_list_returns_list(self):
        
        response = get_orders_list()

        assert response.status_code == Expected.OK, (
            f"Ожидался статус {Expected.OK} при получении списка заказов, "
            f"но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        body = response.json()

        assert Expected.ORDERS_LIST_SUCCESS_ORDERS_KEY in body, (
            f"В ответе отсутствует ключ '{Expected.ORDERS_LIST_SUCCESS_ORDERS_KEY}'. "
            f"Тело ответа: {body}"
        )

        assert isinstance(
            body[Expected.ORDERS_LIST_SUCCESS_ORDERS_KEY],
            Expected.ORDERS_LIST_SUCCESS_ORDERS_TYPE,
        ), (
            f"Поле '{Expected.ORDERS_LIST_SUCCESS_ORDERS_KEY}' должно быть типа "
            f"{Expected.ORDERS_LIST_SUCCESS_ORDERS_TYPE.__name__}, "
            f"но получено: {type(body[Expected.ORDERS_LIST_SUCCESS_ORDERS_KEY]).__name__}. "
            f"Тело ответа: {body}"
        )
        