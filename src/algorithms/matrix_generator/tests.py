import unittest

import numpy as np

from src.algorithms.matrix_generator.function import (
    DETERMINANT,
    GENERATED_MATRIX,
    get_random_matrix_and_det,
)
from src.internal.errors import AlgorithmValueError


class TestCase(unittest.TestCase):
    """Набор тестов для проверки генератора матриц"""

    def test_none(self):
        """Проверка выброса исключения при передаче в параметр None"""
        self.assertRaisesRegex(
            AlgorithmValueError,
            "Порядок матрицы не является целым числом",
            get_random_matrix_and_det,
            None,
        )

    def test_float(self):
        """Проверка выброса исключения при передаче в параметр
        вещественного числа"""
        self.assertRaisesRegex(
            AlgorithmValueError,
            "Порядок матрицы не является целым числом",
            get_random_matrix_and_det,
            1.1,
        )

    def test_zero(self):
        """Проверка выброса исключения при передаче в параметр нуля"""
        self.assertRaisesRegex(
            AlgorithmValueError,
            "Порядок матрицы должен быть целым числом и больше 0",
            get_random_matrix_and_det,
            0,
        )

    def test_neg(self):
        """Проверка выброса исключения при передаче в параметр
        отрицательного значения"""
        self.assertRaisesRegex(
            AlgorithmValueError,
            "Порядок матрицы должен быть целым числом и больше 0",
            get_random_matrix_and_det,
            -1,
        )

    def test_det_with_numpy(self):
        """Проверка генератора на порядках 1-9. Проверяется порядок матрицы
        и расчет определителя"""
        for order in range(1, 10):
            gen_result = get_random_matrix_and_det(order)
            matrix = gen_result[GENERATED_MATRIX]

            self.assertEqual(order, len(matrix))
            for row in matrix:
                self.assertEqual(order, len(row))

            self.assertEqual(
                round(np.linalg.det(np.array(matrix))), gen_result[DETERMINANT]
            )


if __name__ == "__main__":
    unittest.main()
