from typing import Any
import random

from src.internal.errors import AlgorithmTypeError, AlgorithmValueError

TASKS = "tasks"


def __validate_params(task_number: int, min_duration: int, max_duration: int) -> None:
    pass


def generate_tasks(task_number, min_duration=1, max_duration=20):
    __validate_params(task_number, min_duration, max_duration)
    pass


def main(task_number: int, min_duration: int, max_duration: int) -> dict[str, Any]:
    return {TASKS: str(generate_tasks(task_number, min_duration, max_duration))}


if __name__ == "__main__":
    print(main(10, 10, 20))
