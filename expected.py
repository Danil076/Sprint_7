class Expected:

    CREATED = 201
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    CONFLICT = 409

    COURIER_CREATE_SUCCESS = {"ok": True}

    COURIER_DUPLICATE_LOGIN_ERROR = {
        "code": 409,
        "message": "Этот логин уже используется. Попробуйте другой.",
    }

    COURIER_MISSING_REQUIRED_FIELD_ERROR = {
        "code": 400,
        "message": "Недостаточно данных для создания учетной записи",
    }

    LOGIN_SUCCESS_ID_KEY = "id"
    LOGIN_SUCCESS_ID_TYPE = int

    LOGIN_MISSING_REQUIRED_FIELD_ERROR = {
        "code": 400,
        "message": "Недостаточно данных для входа",
    }

    LOGIN_ACCOUNT_NOT_FOUND_ERROR = {
        "code": 404,
        "message": "Учетная запись не найдена",
    }

    ORDER_CREATE_SUCCESS_TRACK_KEY = "track"
    ORDER_CREATE_SUCCESS_TRACK_TYPE = int

    ORDERS_LIST_SUCCESS_ORDERS_KEY = "orders"
    ORDERS_LIST_SUCCESS_ORDERS_TYPE = list
