from typing import Any
import random

from src.internal.errors import AlgorithmTypeError, AlgorithmValueError

TASKS = "tasks"


def __validate_params(task_number: int, min_duration: int, max_duration: int) -> None:
    pass


def generate_tasks(task_number, min_duration=1, max_duration=20):
    __validate_params(task_number, min_duration, max_duration)
    tasks_list = []

    first_less_second_cnt = random.randint(1, round(task_number * 0.45))
    equal_cnt = random.randint(1,  round(task_number * 0.2))
    second_less_first_cnt = task_number - first_less_second_cnt - equal_cnt
    print(first_less_second_cnt, equal_cnt, second_less_first_cnt)

    for task in range(first_less_second_cnt):
        process1 = random.randint(min_duration, max_duration - 1)
        process2 = random.randint(min_duration + 1, max_duration)
        if process1 == process2:
            process1 += 1
        current_task = [min(process1, process2), max(process1, process2)]
        tasks_list.append(current_task)

    for task in range(second_less_first_cnt):
        process1 = random.randint(min_duration, max_duration - 1)
        process2 = random.randint(min_duration + 1, max_duration)
        if process1 == process2:
            process1 += 1
        current_task = [max(process1, process2), min(process1, process2)]
        tasks_list.append(current_task)

    sum_difference = sum(map(lambda x: x[0] - x[1], tasks_list))
    print(sum_difference)

    while sum_difference <= 0:
        for task_index in range(len(tasks_list)):
            current_task = tasks_list[task_index]
            if current_task[0] < current_task[1]:
                if current_task[1] - current_task[0] > 1:
                    current_task[1] -= 1
                    sum_difference += 1
            if current_task[0] > current_task[1]:
                    if current_task[1] > 10:
                        current_task[1] -= 1
                        sum_difference += 1

                    if current_task[0] < 20:
                        current_task[0] += 1
                        sum_difference += 1
            tasks_list[task_index] = current_task

    sum_difference = sum(map(lambda x: x[0] - x[1], tasks_list))
    print(sum_difference)
    for task in range(equal_cnt):
        process1 = random.randint(min_duration, max_duration)

        current_task = [process1, process1]
        tasks_list.append(current_task)

    print(first_less_second_cnt, second_less_first_cnt, equal_cnt)
    return tasks_list


def main(task_number: int, min_duration: int, max_duration: int) -> dict[str, Any]:
    return {TASKS: str(generate_tasks(task_number, min_duration, max_duration))}


if __name__ == "__main__":
    print(main(10, 10, 20))
