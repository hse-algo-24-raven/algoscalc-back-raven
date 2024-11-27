import random

import numpy as np

from src.internal.errors import AlgorithmValueError

GENERATED_MATRIX = "generated_matrix"
DETERMINANT = "determinant"

def check_order(order: int):
    """Проверка на порядок матрицы

    :param order: порядок матрицы
    :raise Exception: если порядок матрицы не является целым числом и порядок
    меньше 1
    """
    if not isinstance(order, int):
        raise AlgorithmValueError("Порядок матрицы не является целым числом")
    if order < 1:
        raise AlgorithmValueError("Порядок матрицы должен быть целым числом и больше 0")


def generate_identity_matrix(order: int) -> list[list[int]]:
    """Генерирует единичную (целочисленную) матрицу с известным размером.

    :param size: порядок матрицы
    :raise Exception: если порядок матрицы не является целым числом и порядок
    меньше 1
    :return: единичная матрица
    """

    check_order(order)
    return [[int(i == j) for i in range(order)] for j in range(order)]

def __make_random_values_matrix_save_det(
    matrix: list[list[int]], rangeStart: int, rangeEnd: int
):
    """Вставляет случайные числа внутрь единичной матрицы, при этом сохраняя
    значение определителя. Достигается за счёт генерации исключительно
    справа/сверху от главной диагонали матрицы.

    :param rangeStart: начальная граница генерации чисел
    :param rangeEnd: конечная граница генерации чисел
    """
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            matrix[i][j] = random.randint(rangeStart, rangeEnd)

def __get_random_multiplier(generationMiddle, generationRange):
    return generationMiddle + random.randint(1, generationRange) * (
        -1 if random.randint(0, 1) == 0 else 1
    )

def __make_random_shake_matrix_save_det(
    matrix: list[list[int]], generationMiddle: int, generationRange: int
):
    """Делает обычную матрицу более разреженной при этом сохраняя
    определитель матрицы за счёт свойства определителя матрицы.
    Определитель матрицы сохраняется, если одну строку умножить на
    любую величину и прибавить к другой строке.

    :param generationMiddle: середина генерации множителя чисел
    :param generationRange: граница генерации множителя чисел
    """

    if generationRange < 1:
        raise AlgorithmValueError(
            "Введённая граница генерации не может быть меньше 1"
        )

    order = len(matrix)

    for i in range(order//2):
        multiplier = __get_random_multiplier(generationMiddle, generationRange)
        for j in range(len(matrix)):
            matrix[i][j] += matrix[order - i - 1][j] * multiplier

    for j in range(order//2):
        multiplier = __get_random_multiplier(generationMiddle, generationRange)
        for i in range(len(matrix)):
            a = matrix[i][order - j - 1] * multiplier
            matrix[i][j] += a

def generate_random_matrix_by_det(order: int, det: int):
    """Генерирует случайную квадратную целочисленную матрицу на основе определителя.

    :param order: порядок матрицы
    :raise Exception: если порядок матрицы не является целым числом и порядок
    меньше 1
    :return: итоговая случайная матрица
    """

    # Проверка order внутри generate_identity_matrix
    matrix = generate_identity_matrix(order)
    matrix[0][0] = det  # Задаётся определитель матрицы путём расположения на главной диагонали
    __make_random_values_matrix_save_det(matrix, -100, 100)
    __make_random_shake_matrix_save_det(matrix, 5, 3)

    return matrix


def get_random_matrix_and_det(order: int):
    """Генерирует случайную квадратную целочисленную матрицу с заранее
    известным значением определителя.

    :param order: порядок матрицы
    :raise Exception: если порядок матрицы не является целым числом и порядок
    меньше 1
    :return: словарь с ключами generated_matrix, determinant
    """

    det = random.randint(-100, 100)
    # Проверка order внутри generate_random_matrix_by_det
    matrix = generate_random_matrix_by_det(order, det)

    return {GENERATED_MATRIX: matrix, DETERMINANT: det}


def main(order: int) -> dict[str, list[list[float]]]:
    return get_random_matrix_and_det(order)


if __name__ == "__main__":
    n = 10
    print(f"Генерация матрицы порядка {n}")
    result = get_random_matrix_and_det(n)
    print("\nОпределитель сгенерированной матрицы равен", result[DETERMINANT])
    print(
        "\n".join(
            ["\t".join([str(cell) for cell in row]) for row in result[GENERATED_MATRIX]]
        )
    )
    print(
        "\nОпределитель, рассчитанный numpy, равен",
        round(np.linalg.det(np.array(result[GENERATED_MATRIX]))),
    )
