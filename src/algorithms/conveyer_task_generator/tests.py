import unittest

from src.algorithms.conveyer_task_generator.function import generate_tasks
from src.internal.errors import AlgorithmTypeError, AlgorithmValueError


class TestCase(unittest.TestCase):

    def test_type(self):
        tasks = generate_tasks(10, 10, 20)
        self.assertIsInstance(tasks, list)
        for task in tasks:
            self.assertIsInstance(task, list)
            self.assertEqual(2, len(task))
            for duration in task:
                self.assertIsInstance(duration, int)

    def test_length(self):
        for length in range(5, 15):
            tasks = generate_tasks(length, 10, 20)
            self.assertEqual(length, len(tasks))

    def test_duration(self):
        cases = ((3, 10), (10, 20), (5, 15))
        for min_dur, max_dur in cases:
            tasks = generate_tasks(10, min_dur, max_dur)
            for task in tasks:
                for duration in task:
                    self.assertGreaterEqual(duration, min_dur)
                    self.assertLessEqual(duration, max_dur)


if __name__ == "__main__":
    unittest.main()
