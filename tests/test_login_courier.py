import allure
import pytest
from api import login_courier
from helpers import generate_random_string
from expected import Expected


@allure.epic("API учебного сервиса Яндекс Самокат")
@allure.feature("Курьеры")
class TestLoginCourier:

    @allure.story("Успешная авторизация курьера")
    @allure.title("Курьер может авторизоваться")
    @allure.description(
        "Создаём тестового курьера, затем отправляем корректный логин и пароль. "
        "Ожидаем HTTP-статус 200 и поле id в теле ответа."
    )
    def test_login_courier_success(self, registered_courier):
        payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        }

        response = login_courier(payload)

        assert response.status_code == Expected.OK, (
            f"Ожидался статус {Expected.OK}, "
            f"но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        body = response.json()

        assert Expected.LOGIN_SUCCESS_ID_KEY in body, (
            f"В ответе отсутствует ключ '{Expected.LOGIN_SUCCESS_ID_KEY}'. "
            f"Тело ответа: {body}"
        )

        assert isinstance(
            body[Expected.LOGIN_SUCCESS_ID_KEY],
            Expected.LOGIN_SUCCESS_ID_TYPE,
        ), (
            f"Поле '{Expected.LOGIN_SUCCESS_ID_KEY}' должно быть типа "
            f"{Expected.LOGIN_SUCCESS_ID_TYPE.__name__}, "
            f"но получено: {type(body[Expected.LOGIN_SUCCESS_ID_KEY]).__name__}. "
            f"Тело ответа: {body}"
        )

    @allure.story("Авторизация с неверным паролем")
    @allure.title("Система вернёт ошибку, если неправильно указать пароль")
    @allure.description(
        "Берём существующего курьера и отправляем неверный пароль. "
        "Ожидаем HTTP-статус 404 и сообщение 'Учетная запись не найдена'."
    )
    def test_login_courier_wrong_password(self, registered_courier):
        payload = {
            "login": registered_courier["login"],
            "password": "wrong_password",
        }

        response = login_courier(payload)

        assert response.status_code == Expected.NOT_FOUND, (
            f"Ожидался статус {Expected.NOT_FOUND} при неверном пароле, "
            f"но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert response.json() == Expected.LOGIN_ACCOUNT_NOT_FOUND_ERROR, (
            f"Ожидалось тело {Expected.LOGIN_ACCOUNT_NOT_FOUND_ERROR}, "
            f"но получено {response.json()}. "
            f"Тело ответа как текст: {response.text}"
        )

    @allure.story("Авторизация несуществующего пользователя")
    @allure.title("Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    @allure.description(
        "Отправляем случайный несуществующий логин и случайный пароль. "
        "Ожидаем HTTP-статус 404 и сообщение 'Учетная запись не найдена'."
    )
    def test_login_courier_non_existent_user(self):
        payload = {
            "login": "non_existent_" + generate_random_string(),
            "password": generate_random_string(),
        }

        response = login_courier(payload)

        assert response.status_code == Expected.NOT_FOUND, (
            f"Ожидался статус {Expected.NOT_FOUND} для несуществующего пользователя, "
            f"но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert response.json() == Expected.LOGIN_ACCOUNT_NOT_FOUND_ERROR, (
            f"Ожидалось тело {Expected.LOGIN_ACCOUNT_NOT_FOUND_ERROR}, "
            f"но получено {response.json()}. "
            f"Тело ответа как текст: {response.text}"
        )

    @allure.story("Авторизация без обязательного поля login")
    @allure.title("Ошибка при отсутствии login")
    @allure.description(
        "Отправляем запрос на логин без поля login. "
        "Ожидаем HTTP-статус 400 и сообщение о недостатке данных для входа."
    )
    def test_login_courier_missing_login(self):
        payload = {
            "password": generate_random_string(),
        }

        response = login_courier(payload)

        assert response.status_code == Expected.BAD_REQUEST, (
            f"Ожидался статус {Expected.BAD_REQUEST} при отсутствии поля login, "
            f"но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert response.json() == Expected.LOGIN_MISSING_REQUIRED_FIELD_ERROR, (
            f"Ожидалось тело {Expected.LOGIN_MISSING_REQUIRED_FIELD_ERROR}, "
            f"но получено {response.json()}. "
            f"Тело ответа как текст: {response.text}"
        )

    @allure.story("Авторизация без обязательного поля password")
    @allure.title("Ошибка при отсутствии password")
    @allure.description(
        "Отправляем запрос на логин без поля password. "
        "По документации ожидается HTTP-статус 400 и сообщение о недостатке данных для входа. "
        "На текущем стенде этот запрос может возвращать 504 или timeout, "
        "поэтому тест помечен как ожидаемо падающий."
    )
    @pytest.mark.xfail(
        reason=(
            "Стенд может возвращать 504 или timeout при запросе без password. "
            "Если в Postman подтвердился стабильный статус 400, удали этот декоратор."
        ),
        strict=False,
    )
    def test_login_courier_missing_password(self, registered_courier):
        payload = {
            "login": registered_courier["login"],
        }

        response = login_courier(payload)

        assert response.status_code == Expected.BAD_REQUEST, (
            f"Ожидался статус {Expected.BAD_REQUEST} при отсутствии поля password, "
            f"но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert response.json() == Expected.LOGIN_MISSING_REQUIRED_FIELD_ERROR, (
            f"Ожидалось тело {Expected.LOGIN_MISSING_REQUIRED_FIELD_ERROR}, "
            f"но получено {response.json()}. "
            f"Тело ответа как текст: {response.text}"
        )
