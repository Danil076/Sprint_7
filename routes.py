from settings import BASE_URL

class Routes:

    # Класс-пространство имён для маршрутов API
    COURIER_CREATE = f"{BASE_URL}/courier"
    COURIER_LOGIN = f"{BASE_URL}/courier/login"
    ORDER_CREATE = f"{BASE_URL}/orders"
    ORDER_LIST = f"{BASE_URL}/orders"
