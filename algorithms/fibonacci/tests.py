import unittest


from algorithms.fibonacci.function import fibonacci


class TestCase(unittest.TestCase):
    numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    def test_fibonacci(self):
        for index, number in enumerate(self.numbers):
            self.assertEqual(fibonacci(index + 1), number)


if __name__ == '__main__':
    unittest.main()
