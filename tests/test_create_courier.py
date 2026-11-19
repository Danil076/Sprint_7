import pytest
import allure
from api import create_courier
from expected import Expected


@allure.epic("API учебного сервиса Яндекс Самокат")
@allure.feature("Курьеры")
class TestCreateCourier:

    @allure.story("Успешное создание курьера")
    @allure.title("Курьера можно создать")
    @allure.description(
        "Отправляем валидные данные для создания курьера. "
        "Ожидаем HTTP-статус 201 и тело ответа {'ok': True}."
    )

    def test_create_courier_success(self, courier_payload):

        # Проверка, что курьера можно создать успешно
        response = create_courier(courier_payload)

        assert response.status_code == Expected.CREATED, (
            f"Ожидался статус {Expected.CREATED}, "
            f"но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert response.json() == Expected.COURIER_CREATE_SUCCESS, (
            f"Ожидалось тело {Expected.COURIER_CREATE_SUCCESS}, "
            f"но получено {response.json()}. "
            f"Тело ответа как текст: {response.text}"
        )

    @allure.story("Создание курьера с уже существующим логином")
    @allure.title("Нельзя создать двух одинаковых курьеров")
    @allure.description(
        "Создаём курьера, затем повторно отправляем запрос с тем же логином. "
        "Ожидаем HTTP-статус 409 и сообщение о том, что логин уже используется."
    )
    def test_create_courier_duplicate_login(self, courier_payload):

        # Проверка, что нельзя создать двух курьеров с одинаковым логином.
        first_response = create_courier(courier_payload)

        assert first_response.status_code == Expected.CREATED, (
            f"Первый запрос должен был создать курьера со статусом "
            f"{Expected.CREATED}, но получил {first_response.status_code}. "
            f"Тело ответа: {first_response.text}"
        )

        second_response = create_courier(courier_payload)

        assert second_response.status_code == Expected.CONFLICT, (
            f"Ожидался статус {Expected.CONFLICT} при повторном создании курьера с тем же логином, "
            f"но получен {second_response.status_code}. "
            f"Тело ответа: {second_response.text}"
        )

        assert second_response.json() == Expected.COURIER_DUPLICATE_LOGIN_ERROR, (
            f"Ожидалось тело {Expected.COURIER_DUPLICATE_LOGIN_ERROR}, "
            f"но получено {second_response.json()}. "
            f"Тело ответа как текст: {second_response.text}"
        )

    @allure.story("Создание курьера без обязательных полей login и password")
    @pytest.mark.parametrize(
        "missing_field",
        [
            "login",
            "password",
        ],
    )
    def test_create_courier_missing_required_field(
        self,
        courier_payload,
        missing_field,
    ):
        allure.dynamic.title(
            f"Ошибка при отсутствии обязательного поля: {missing_field}"
        )

        allure.dynamic.description(
            f"Проверяем, что при создании курьера без поля '{missing_field}' "
            f"сервер возвращает HTTP-статус 400 и сообщение о недостатке данных."
        )

        # Проверяем отсутствие обязательного поля login или password
        payload = courier_payload.copy()
        del payload[missing_field]

        response = create_courier(payload)

        assert response.status_code == Expected.BAD_REQUEST, (
            f"Ожидался статус {Expected.BAD_REQUEST} при отсутствии поля "
            f"'{missing_field}', но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert response.json() == Expected.COURIER_MISSING_REQUIRED_FIELD_ERROR, (
            f"Ожидалось тело {Expected.COURIER_MISSING_REQUIRED_FIELD_ERROR} "
            f"при отсутствии поля '{missing_field}', "
            f"но получено {response.json()}. "
            f"Тело ответа как текст: {response.text}"
        )

    @allure.story("Создание курьера без обязательного поля firstName")
    @allure.title("Ошибка при отсутствии firstName")
    @allure.description(
        "Проверяем, что при создании курьера без поля firstName "
        "сервер должен возвращать HTTP-статус 400 и сообщение о недостатке данных. "
        "На текущем стенде API может создавать курьера без firstName, "
        "поэтому тест помечен как ожидаемо падающий."
    )
    @pytest.mark.xfail(
        reason=(
            "Стенд позволяет создать курьера без firstName, "
            "хотя по документации поле обязательное."
        ),
        strict=False,
    )
    def test_create_courier_missing_first_name(self, courier_payload):

        # Проверяем отсутствие обязательного поля firstName
        payload = courier_payload.copy()
        del payload["firstName"]

        response = create_courier(payload)

        assert response.status_code == Expected.BAD_REQUEST, (
            f"Ожидался статус {Expected.BAD_REQUEST} при отсутствии поля firstName, "
            f"но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert response.json() == Expected.COURIER_MISSING_REQUIRED_FIELD_ERROR, (
            f"Ожидалось тело {Expected.COURIER_MISSING_REQUIRED_FIELD_ERROR} "
            f"при отсутствии поля firstName, "
            f"но получено {response.json()}. "
            f"Тело ответа как текст: {response.text}"
        )
        