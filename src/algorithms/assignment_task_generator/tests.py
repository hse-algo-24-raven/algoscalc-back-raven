import unittest

from src.algorithms.assignment_task_generator.function import (
    MAX_COST_ERR_MSG,
    MAX_COST_TYPE_ERR_MSG,
    MIN_COST_ERR_MSG,
    MIN_COST_TYPE_ERR_MSG,
    MIN_MAX_COST_ERR_MSG,
    ORDER_ERR_MSG,
    ORDER_TYPE_ERR_MSG,
    generate_matrix,
)
from src.internal.errors import AlgorithmTypeError, AlgorithmValueError


class TestCase(unittest.TestCase):
    def test_type(self):
        matrix = generate_matrix(5, 5, 15)
        self.assertIsInstance(matrix, list)
        for row in matrix:
            self.assertIsInstance(row, list)
            for val in row:
                self.assertIsInstance(val, int)

    def test_order(self):
        for order in range(5, 15):
            matrix = generate_matrix(order, 10, 20)
            self.assertEqual(order, len(matrix))
            for row in matrix:
                self.assertEqual(order, len(row))

    def test_cost(self):
        cases = ((3, 10), (10, 20), (5, 15))
        for min_cost, max_cost in cases:
            matrix = generate_matrix(10, min_cost, max_cost)
            for row in matrix:
                for val in row:
                    self.assertGreaterEqual(val, min_cost)
                    self.assertLessEqual(val, max_cost)

    def test_order_type(self):
        incorrect_values = [None, "str", 1.1]
        for val in incorrect_values:
            self.assertRaisesRegex(
                AlgorithmTypeError, ORDER_TYPE_ERR_MSG, generate_matrix, val, 1, 2
            )

    def test_order_value(self):
        incorrect_values = [-1, 0]
        for val in incorrect_values:
            self.assertRaisesRegex(
                AlgorithmValueError, ORDER_ERR_MSG, generate_matrix, val, 1, 2
            )

    def test_min_cost_type(self):
        incorrect_values = [None, "str", 1.1]
        for val in incorrect_values:
            self.assertRaisesRegex(
                AlgorithmTypeError, MIN_COST_TYPE_ERR_MSG, generate_matrix, 1, val, 2
            )

    def test_min_cost_value(self):
        incorrect_values = [-1, 0]
        for val in incorrect_values:
            self.assertRaisesRegex(
                AlgorithmValueError, MIN_COST_ERR_MSG, generate_matrix, 1, val, 2
            )

    def test_max_cost_type(self):
        incorrect_values = [None, "str", 1.1]
        for val in incorrect_values:
            self.assertRaisesRegex(
                AlgorithmTypeError, MAX_COST_TYPE_ERR_MSG, generate_matrix, 1, 1, val
            )

    def test_max_cost_value(self):
        incorrect_values = [-1, 0]
        for val in incorrect_values:
            self.assertRaisesRegex(
                AlgorithmValueError, MAX_COST_ERR_MSG, generate_matrix, 1, 1, val
            )

    def test_min_max_diff(self):
        self.assertRaisesRegex(
            AlgorithmValueError, MIN_MAX_COST_ERR_MSG, generate_matrix, 3, 2, 1
        )


if __name__ == "__main__":
    unittest.main()
