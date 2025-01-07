from typing import Any
import random

from src.internal.errors import AlgorithmTypeError, AlgorithmValueError

TASKS = "tasks"


def __validate_params(task_number: int, min_duration: int, max_duration: int) -> None:
    pass


def generate_tasks(task_number, min_duration=1, max_duration=20):
    __validate_params(task_number, min_duration, max_duration)
    tasks_list = []
    first_less_second_cnt = random.randint(1, task_number - 2)
    second_less_first_cnt = random.randint(1, task_number - first_less_second_cnt - 1)
    equal_cnt = task_number - first_less_second_cnt - second_less_first_cnt

    for task in range(first_less_second_cnt):
        procces1 = random.randint(min_duration, max_duration - 1)
        procces2 = random.randint(min_duration + 1, max_duration)
        if procces1 == procces2:
            procces1 += 1
        current_task = [min(procces1, procces2), max(procces1, procces2)]
        tasks_list.append(current_task)

    for task in range(second_less_first_cnt):
        procces1 = random.randint(min_duration, max_duration - 1)
        procces2 = random.randint(min_duration + 1, max_duration)
        if procces1 == procces2:
            procces1 += 1
        current_task = [max(procces1, procces2), min(procces1, procces2)]
        tasks_list.append(current_task)

    sum_difference = sum(map(lambda x: x[0] - x[1], tasks_list))
    print(sum_difference)


    sum_difference = sum(map(lambda x: x[0] - x[1], tasks_list))
    print(sum_difference)
    for task in range(equal_cnt):
        procces1 = random.randint(min_duration, max_duration)

        current_task = [procces1, procces1]
        tasks_list.append(current_task)

    print(first_less_second_cnt, second_less_first_cnt, equal_cnt)
    print(tasks_list)


def main(task_number: int, min_duration: int, max_duration: int) -> dict[str, Any]:
    return {TASKS: str(generate_tasks(task_number, min_duration, max_duration))}


if __name__ == "__main__":
    print(main(10, 10, 20))
