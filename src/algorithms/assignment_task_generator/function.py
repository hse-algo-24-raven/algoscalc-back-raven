import random
from collections import deque
from typing import Any

from src.internal.errors import AlgorithmTypeError, AlgorithmValueError
from src.internal.errors.exceptions import AlgorithmRuntimeError

COSTS = "costs"

ORDER_TYPE_ERR_MSG = "Порядок матрицы не является целым числом"
MIN_COST_TYPE_ERR_MSG = "Минимальная стоимость назначения не является целым числом"
MAX_COST_TYPE_ERR_MSG = "Максимальная стоимость назначения не является целым числом"
MIN_COST_ERR_MSG = "Минимальная стоимость назначения должна быть больше нуля"
MAX_COST_ERR_MSG = "Максимальная стоимость назначения должна быть больше нуля"
ORDER_ERR_MSG = "Количество задач должно быть больше нуля"
MIN_MAX_COST_ERR_MSG = "Минимальная длительность этапа должна быть меньше максимальной"


def __validate_params(order: int, min_cost: int, max_cost: int) -> None:
    pass


def generate_matrix(order: int, min_cost: int, max_cost: int):
    """
    Генератор условий задачи о назначениях
    :param order: Порядок матрицы затрат.
    :param min_cost: Минимальная стоимость назначения.
    :param max_cost: Максимальная стоимость назначения.
    :return: Квадратная матрица затрат заданного порядка.
    """
    __validate_params(order, min_cost, max_cost)

    pass


def main(order: int, min_cost: int, max_cost: int) -> dict[str, Any]:
    return {COSTS: generate_matrix(order, min_cost, max_cost)}


if __name__ == "__main__":
    print(main(15, 5, 15))
