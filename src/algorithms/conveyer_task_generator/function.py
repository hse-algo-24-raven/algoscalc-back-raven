import random
from typing import Any

from src.internal.errors import AlgorithmTypeError, AlgorithmValueError

TASKS = "tasks"
ERR_MSG_TASK_NUMBER_MUST_INT = "Число задач должно быть целым числом"
ERR_MSG_MIN_DURATION_MUST_INT = "Минимальная длительность должна быть целым числом"
ERR_MSG_MAX_DURATION__MUST_INT = "Максимальная длительность должна быть целым числом"
ERR_MSG_TO_LITTLE_TASK_NUMBER = "Число задач должно быть целым числом"
ERR_MSG_MIN_MORE_MAX = "Число задач должно быть целым числом"
ERR_MSG_MIN_IS_NOT_POSITIVE = "Число задач должно быть целым числом"
ERR_MSG_MAX_IS_NOT_POSITIVE = "Число задач должно быть целым числом"


def __validate_params(task_number: int, min_duration: int, max_duration: int) -> None:
    if not isinstance(task_number, int):
        raise AlgorithmTypeError(ERR_MSG_TASK_NUMBER_MUST_INT)
    if not isinstance(min_duration, int):
        raise AlgorithmTypeError(ERR_MSG_MIN_DURATION_MUST_INT)
    if not isinstance(max_duration, int):
        raise AlgorithmTypeError(ERR_MSG_MAX_DURATION__MUST_INT)

    if task_number < 3:
        raise AlgorithmValueError(ERR_MSG_TO_LITTLE_TASK_NUMBER)
    if min_duration >= max_duration:
        raise AlgorithmValueError(ERR_MSG_MIN_MORE_MAX)
    if max_duration < 1:
        raise AlgorithmValueError(ERR_MSG_MIN_IS_NOT_POSITIVE)
    if min_duration < 1:
        raise AlgorithmValueError(ERR_MSG_MAX_IS_NOT_POSITIVE)


def generate_tasks(task_number, min_duration=1, max_duration=20):
    __validate_params(task_number, min_duration, max_duration)
    tasks_list = []

    first_less_second_cnt = random.randint(1, round(task_number * 0.45))
    equal_cnt = random.randint(1, round(task_number * 0.2))
    second_less_first_cnt = task_number - first_less_second_cnt - equal_cnt

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

    tasks_list = _generate_pass(tasks_list)

    for task in range(equal_cnt):
        process1 = random.randint(min_duration, max_duration)

        current_task = [process1, process1]
        tasks_list.append(current_task)

    return tasks_list


def _generate_pass(tasks_list: list[list]) -> list[list]:
    """
    Args:
        tasks_list: Список задач, который нужно проверить на наличие пропуска в середине

    Returns:
    Список задач, с пропуском в середине
    """
    new_tasks_list = tasks_list[:]
    sum_difference = sum(map(lambda x: x[0] - x[1], new_tasks_list))

    while sum_difference <= 0:
        for task_index in range(len(new_tasks_list)):
            new_tasks_list[task_index], sum_difference = _change_difference(
                new_tasks_list[task_index], sum_difference
            )
    return new_tasks_list


def _change_difference(
    current_task: list[int], sum_difference: int
) -> tuple[list[int], int]:
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

    return current_task, sum_difference


def main(task_number: int, min_duration: int, max_duration: int) -> dict[str, Any]:
    return {TASKS: str(generate_tasks(task_number, min_duration, max_duration))}


if __name__ == "__main__":
    print(main(10, 10, 20))
