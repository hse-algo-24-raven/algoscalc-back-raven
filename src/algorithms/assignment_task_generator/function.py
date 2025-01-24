import random
from collections import deque
from typing import Any

from src.internal.errors import AlgorithmTypeError, AlgorithmValueError

COSTS = "costs"

ORDER_TYPE_ERR_MSG = "Порядок матрицы не является целым числом"
MIN_COST_TYPE_ERR_MSG = "Минимальная стоимость назначения не является целым числом"
MAX_COST_TYPE_ERR_MSG = "Максимальная стоимость назначения не является целым числом"
MIN_COST_ERR_MSG = "Минимальная стоимость назначения должна быть больше нуля"
MAX_COST_ERR_MSG = "Максимальная стоимость назначения должна быть больше нуля"
ORDER_ERR_MSG = "Количество задач должно быть больше двух"
MIN_MAX_COST_ERR_MSG = "Минимальная длительность этапа должна быть меньше максимальной"


def __validate_params(order: int, min_cost: int, max_cost: int) -> None:
    if not isinstance(order, int):
        raise AlgorithmTypeError(ORDER_TYPE_ERR_MSG)
    if not isinstance(min_cost, int):
        raise AlgorithmTypeError(MIN_COST_TYPE_ERR_MSG)
    if not isinstance(max_cost, int):
        raise AlgorithmTypeError(MAX_COST_TYPE_ERR_MSG)
    if min_cost <= 0:
        raise AlgorithmValueError(MIN_COST_ERR_MSG)
    if max_cost <= 0:
        raise AlgorithmValueError(MAX_COST_ERR_MSG)
    if order <= 2:
        raise AlgorithmValueError(ORDER_ERR_MSG)
    if max_cost <= min_cost:
        raise AlgorithmValueError(MIN_MAX_COST_ERR_MSG)


def __random_bool():
    return bool(random.randint(0, 1))


def __distribute_nulls_in_matrix(order: int):
    """
    Возвращает матрицу распределения нулей.
    В матрице False - значит, что на этом
    месте будет 0, иначе - True.

    Гарантированно, что будет хотя бы одна колонка
    и одна строка с нулями
    """

    matrix = [[True for _ in range(order)] for _ in range(order)]

    num_connecting_lines = random.randint(2, order - 1)
    num_row_lines = random.randint(1, num_connecting_lines - 1)
    num_column_lines = num_connecting_lines - num_row_lines
    row_lines_index: list[int] = [None] * num_row_lines
    column_lines_index: list[int] = [None] * num_column_lines

    free_rows = list(range(order))
    free_columns = list(range(order))

    is_column_line = [False] * order

    random.shuffle(free_rows)
    random.shuffle(free_columns)

    # Генерация столбцов с нулями
    for index in range(num_column_lines):
        column = free_columns.pop()
        column_lines_index[index] = column
        is_column_line[column] = True

        line_nulls_len = random.randint(1, order)
        line = ([False] * line_nulls_len) + ([True] * (order - line_nulls_len))
        random.shuffle(line)
        for row in range(order):
            matrix[row][column] = line[row]

    # Первичное создание строк
    for index in range(num_row_lines):
        row = free_rows.pop()
        row_lines_index[index] = row

    free_row_lines = row_lines_index.copy()
    random.shuffle(free_row_lines)

    # Заполнение клеток по столбцам, где необходимы нули
    for column in range(order):
        if not is_column_line[column]:
            row = free_row_lines[-1]
            random.shuffle(free_row_lines)
            matrix[row][column] = False

    # Генерация по остаточному принципу
    # (где в матрице указан False, там он и останется,
    # в ином случае False ставится случайно вдоль row_line)
    for row in row_lines_index:
        if not (False in matrix[row]):
            matrix[row][random.randint(0, order - 1)] = False
        for column in range(order):
            if not matrix[row][column]:
                matrix[row][column] = False
            else:
                matrix[row][column] = __random_bool()

    # Добавить нули, если их вдруг где-то не оказалось
    free_column_lines = column_lines_index.copy()
    random.shuffle(free_column_lines)
    for row in range(order):
        if matrix[row].count(False) == 0:
            random_column_line = free_column_lines[-1]
            random.shuffle(free_column_lines)
            matrix[row][random_column_line] = False

    return matrix


def generate_matrix(order: int, min_cost: int, max_cost: int):
    """
    Генератор условий задачи о назначениях
    :param order: Порядок матрицы затрат.
    :param min_cost: Минимальная стоимость назначения.
    :param max_cost: Максимальная стоимость назначения.
    :return: Квадратная матрица затрат заданного порядка.
    """
    __validate_params(order, min_cost, max_cost)

    matrix = __distribute_nulls_in_matrix(order)

    free_columns = list()

    # Поиск кандидатов для доп. колонки,
    # которую нужно будет редуцировать
    for column in range(order):
        count = 0
        for row in range(order):
            if not matrix[row][column]:
                count += 1
            if not matrix[row][column] and matrix[row].count(False) <= 1:
                count = 0
                break
        if count != 0 and count < order:
            free_columns.append(column)

    random.shuffle(free_columns)

    if len(free_columns) != 0:
        # Воссоздание редукции по колонке
        addition_column = free_columns.pop()
        min_addition_column_value = random.randint(1, (max_cost + min_cost) // 4)
    else:
        addition_column = -1
        min_addition_column_value = 0

    # Перевод в ответ
    for row in range(order):
        diff_max = max_cost - min_addition_column_value
        min_value = random.randint(min_cost, diff_max - 1)

        for column in range(order):
            if column != addition_column:
                if matrix[row][column]:
                    matrix[row][column] = random.randint(min_value + 1, max_cost)
                else:
                    matrix[row][column] = min_value
            else:
                if matrix[row][column]:
                    matrix[row][column] = random.randint(min_value + min_addition_column_value + 1, max_cost)
                else:
                    matrix[row][column] = min_addition_column_value+min_value

    return matrix


def main(order: int, min_cost: int, max_cost: int) -> dict[str, Any]:
    return {COSTS: generate_matrix(order, min_cost, max_cost)}


if __name__ == "__main__":
    print(main(15, 5, 15))
