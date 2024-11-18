import unittest

from src.algorithms.fibonacci.function import main


class TestCase(unittest.TestCase):
    numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    def test_fibonacci(self):
        for index, number in enumerate(self.numbers):
            self.assertEqual(main(str(index + 1)), {"result": number})


if __name__ == "__main__":
    unittest.main()
