import random

import numpy as np

from src.internal.errors import AlgorithmValueError

GENERATED_MATRIX = "generated_matrix"
DETERMINANT = "determinant"


def get_random_matrix_and_det(order):
    """Генерирует случайную квадратную целочисленную матрицу с заранее
    известным значением определителя.

    :param order: порядок матрицы
    :raise Exception: если порядок матрицы не является целым числом и порядок
    меньше 1
    :return: словарь с ключами generated_matrix, determinant
    """
    pass


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
