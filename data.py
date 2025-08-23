from helpers import generate_random_string

BASE_ORDER_DATA = {
    "firstName": generate_random_string(10),
    "lastName": generate_random_string(10),
    "address": generate_random_string(15),
    "metroStation": 4,
    "phone": "+7999" + "".join([str(i) for i in range(7)]),
    "rentTime": 5,
    "deliveryDate": "2024-12-31",
    "comment": generate_random_string(20)
}

COLOR_TEST_DATA = [
    (["BLACK"], "Черный цвет"),
    (["GREY"], "Серый цвет"),
    (["BLACK", "GREY"], "Оба цвета"),
    ([], "Без цвета")
]