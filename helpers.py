import random
import string
from datetime import date, timedelta

from data import (
    ADDRESS_MAX_APARTMENT,
    COMMENT_LENGTH,
    DELIVERY_DAYS_AHEAD,
    ORDER_METRO_STATION,
    ORDER_RENT_TIME,
    PHONE_DIGITS_AFTER_CODE,
    RANDOM_STRING_LENGTH,
)


def generate_random_string(length=RANDOM_STRING_LENGTH):
    # Генерирует случайную строку из строчных латинских букв
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_random_digits(length):
    # Генерирует случайную строку из цифр
    digits = string.digits
    return "".join(random.choice(digits) for _ in range(length))


def generate_phone_number():
    # Генерирует телефон в формате +7XXXXXXXXXX
    return "+7" + generate_random_digits(PHONE_DIGITS_AFTER_CODE)


def generate_future_delivery_date(days_ahead=DELIVERY_DAYS_AHEAD):
    # Генерирует дату доставки в будущем
    target_date = date.today() + timedelta(days=days_ahead)
    return target_date.isoformat()

def build_courier_payload():
    # Собирает тело запроса для создания нового курьера
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }


def build_order_payload(color=None):
    # Собирает тело запроса для создания заказа
    payload = {
        "firstName": generate_random_string(),
        "lastName": generate_random_string(),
        "address": (
            f"{generate_random_string()} street, "
            f"{random.randint(1, ADDRESS_MAX_APARTMENT)} apt."
        ),
        "metroStation": ORDER_METRO_STATION,
        "phone": generate_phone_number(),
        "rentTime": ORDER_RENT_TIME,
        "deliveryDate": generate_future_delivery_date(),
        "comment": generate_random_string(COMMENT_LENGTH),
    }

    if color is not None:
        payload["color"] = color

    return payload

def build_color_label(color):

    if color is None:
        return "без цвета"

    return ", ".join(color)
