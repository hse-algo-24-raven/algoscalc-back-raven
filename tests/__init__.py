from enum import auto

from strenum import LowercaseStrEnum

from tests.case import Case


class ErrorItemEnum(LowercaseStrEnum):
    LOC = auto()
    MSG = auto()


INT_CASE = Case(123, "Int value")
NONE_CASE = Case(None, "None value")
STR_CASE = Case("value", "String value")
STR_EMPTY_CASE = Case("", "Empty string")
STR_WHITESPASE_CASE = Case("   ", "Whitespace string")
FLOAT_CASE = Case(45.67, "Float value")
BOOL_TRUE_CASE = Case(True, "Boolean true")
BOOL_FALSE_CASE = Case(False, "Boolean false")
LIST_INT_CASE = Case([1, 2, 3], "List value")
DISCT_CASE = Case({"key": "value"}, "Dictionary value")
TUPLE_INT_CASE = Case((1, 2), "Tuple value")
SET_INT_CASE = Case({1, 2, 3}, "Set value")
MATRIX_INT_CASE = Case([[1], [2]], "Int matrix")

BOOL_CASES = [
    BOOL_TRUE_CASE,
    BOOL_FALSE_CASE,
]
INVALID_STRING_CASES = [
    INT_CASE,
    NONE_CASE,
    STR_EMPTY_CASE,
    STR_WHITESPASE_CASE,
    FLOAT_CASE,
    BOOL_TRUE_CASE,
    LIST_INT_CASE,
    DISCT_CASE,
    TUPLE_INT_CASE,
    SET_INT_CASE,
]
EMPTY_STRING_CASES = [
    STR_EMPTY_CASE,
    STR_WHITESPASE_CASE,
]
NOT_STRING_CASES = [
    INT_CASE,
    FLOAT_CASE,
    BOOL_TRUE_CASE,
]
NOT_SCALAR_CASES = [
    LIST_INT_CASE,
    TUPLE_INT_CASE,
    SET_INT_CASE,
]
NOT_NUMBER_CASES = [
    STR_CASE,
    STR_EMPTY_CASE,
    STR_WHITESPASE_CASE,
    BOOL_TRUE_CASE,
]
NOT_INT_CASES = NOT_NUMBER_CASES + [FLOAT_CASE]

NOT_BOOL_CASES = [
    INT_CASE,
    STR_CASE,
    FLOAT_CASE,
]

SCALAR_CASES = [
    INT_CASE,
    STR_CASE,
    FLOAT_CASE,
    BOOL_TRUE_CASE,
]

CHECK_ENUM_INVALID_CASES = INVALID_STRING_CASES + [STR_CASE]


NAME = "name"
TITLE = "title"
DESCRIPTION = "description"
DATA_TYPE = "data_type"
DATA_SHAPE = "data_shape"
DEFAULT_VALUE = "default_value"
PARAMETERS = "parameters"
OUTPUTS = "outputs"

FIB_NAME = "fibonacci"
FIB_TITLE = "Числа Фибоначчи"
FIB_DEF = {
    "name": FIB_NAME,
    "title": FIB_TITLE,
    "description": "Вычисление n-го числа Фибоначчи",
    "parameters": [
        {
            "name": "n",
            "title": "Номер числа Фибоначчи",
            "description": "Введите целое положительное число больше единицы",
            "data_type": "INT",
            "data_shape": "SCALAR",
            "default_value": 1,
        }
    ],
    "outputs": [
        {
            "name": "result",
            "title": "Число Фибоначчи",
            "description": "Число Фибоначчи с номером n",
            "data_type": "INT",
            "data_shape": "SCALAR",
            "default_value": 1,
            "is_deterministic": True,
        }
    ],
}
FIB_FUNC = """def fibonacci(n: int) -> int:
    if n == 1 or n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)
def main(n: int):
    return {'result': fibonacci(n)}"""
FIB_TESTS = """import unittest
from src.algorithms.fibonacci.function import fibonacci
class TestCase(unittest.TestCase):
    numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    def test_fibonacci(self):
        for index, number in enumerate(self.numbers):
            self.assertEqual(fibonacci(index + 1), number)"""
WRONG_FIB_TESTS = """import unittest
from src.algorithms.fibonacci.function import fibonacci
class TestCase(unittest.TestCase):
    numbers = [0, 0]
    def test_fibonacci(self):
        for index, number in enumerate(self.numbers):
            self.assertEqual(fibonacci(index + 1), number)"""

SUM_NAME = "sum"
SUM_TITLE = "Сумма двух чисел"
SUM_DEF = {
    "name": SUM_NAME,
    "title": SUM_TITLE,
    "description": "Вычисление суммы двух чисел",
    "parameters": [
        {
            "name": "a",
            "title": "Число a",
            "description": "Введите целое положительное число больше единицы",
            "data_type": "INT",
            "data_shape": "SCALAR",
            "default_value": 1,
        },
        {
            "name": "b",
            "title": "Число b",
            "description": "Введите целое положительное число больше единицы",
            "data_type": "INT",
            "data_shape": "SCALAR",
            "default_value": 1,
        },
    ],
    "outputs": [
        {
            "name": "result",
            "title": "Сумма двух чисел",
            "description": "Сумма двух чисел",
            "data_type": "INT",
            "data_shape": "SCALAR",
            "default_value": 2,
            "is_deterministic": True,
        }
    ],
}
SUM_FUNC = """
def main(a: int, b: int):
    return {'result': a + b}"""


BOOL_NAME = "bool"
BOOL_DEF = {
    "name": BOOL_NAME,
    "title": BOOL_NAME,
    "description": BOOL_NAME,
    "parameters": [
        {
            "name": "x",
            "title": "x",
            "description": "x",
            "data_type": "BOOL",
            "data_shape": "SCALAR",
            "default_value": True,
        },
    ],
    "outputs": [
        {
            "name": "y",
            "title": "y",
            "description": "y",
            "data_type": "BOOL",
            "data_shape": "SCALAR",
            "default_value": True,
            "is_deterministic": True,
        }
    ],
}
BOOL_FUNC = """
def main(x: bool):
    return {'y': x}"""

MOCK_TESTS = """import unittest
class TestCase(unittest.TestCase):
    def test_func(self):
        self.assertEqual(1, 1)"""
