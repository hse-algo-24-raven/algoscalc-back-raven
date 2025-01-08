import random
from typing import Any

from src.internal.errors import AlgorithmTypeError, AlgorithmValueError

TASKS = "tasks"

TASK_NUMBER_TYPE_ERR_MSG = "Количество задач не является целым числом"
MIN_DURATION_TYPE_ERR_MSG = (
    "Минимальная длительность одного этапа не является целым числом"
)
MAX_DURATION_TYPE_ERR_MSG = (
    "Максимальная длительность одного этапа не является целым числом"
)
MIN_DURATION_LIMITS_ERR_MSG = "Минимальная длительность этапа должна быть больше нуля"
MAX_DURATION_LIMITS_ERR_MSG = "Максимальная длительность этапа должна быть больше нуля"
TASK_NUMBER_LIMITS_ERR_MSG = "Количество задач должно быть больше три и более"
MIN_MAX_DURATION_ERR_MSG = (
    "Минимальная длительность этапа должна быть меньше максимальной"
)


def __validate_params(task_number: int, min_duration: int, max_duration: int) -> None:
    if not isinstance(task_number, int):
        raise AlgorithmTypeError(TASK_NUMBER_TYPE_ERR_MSG)
    if not isinstance(min_duration, int):
        raise AlgorithmTypeError(MIN_DURATION_TYPE_ERR_MSG)
    if not isinstance(max_duration, int):
        raise AlgorithmTypeError(MAX_DURATION_TYPE_ERR_MSG)
    if min_duration <= 0:
        raise AlgorithmValueError(MIN_DURATION_LIMITS_ERR_MSG)
    if max_duration <= 0:
        raise AlgorithmValueError(MAX_DURATION_LIMITS_ERR_MSG)
    if task_number < 3:
        raise AlgorithmValueError(TASK_NUMBER_LIMITS_ERR_MSG)
    if min_duration > max_duration:
        raise AlgorithmValueError(MIN_MAX_DURATION_ERR_MSG)


def __has_downtime(original_tasks: list) -> bool:
    tasks = original_tasks.copy()

    # Разделение задач на две группы
    group1 = [task for task in tasks if task[0] <= task[1]]  # a_i <= b_i
    group2 = [task for task in tasks if task[0] > task[1]]  # a_i > b_i

    # Сортировка групп
    group1 = sorted(group1, key=lambda x: x[0])  # По возрастанию a_i
    group2 = sorted(group2, key=lambda x: x[1], reverse=True)  # По убыванию b_i

    # Объединение задач по алгоритму Джонсона
    tasks = group1 + group2

    offsets = []
    current_time_worker_1, current_time_worker_2 = 0, 0
    for idx, (first_stage, second_stage) in enumerate(tasks):
        # Работник 1 выполняет первый этап
        start_time_worker_1 = current_time_worker_1
        end_time_worker_1 = start_time_worker_1 + first_stage
        current_time_worker_1 = end_time_worker_1

        # Работник 2 выполняет второй этап
        start_time_worker_2 = max(current_time_worker_2, end_time_worker_1)
        end_time_worker_2 = start_time_worker_2 + second_stage

        if len(offsets) != 0 and start_time_worker_2 > offsets[-1][1]:
            return True
        offsets.append((start_time_worker_2, end_time_worker_2))
        current_time_worker_2 = end_time_worker_2
    return False


def __create_pseudorandom_in_start(tasks, min_duration, max_duration):
    firstStageNewTime = random.randint(min_duration, (max_duration + min_duration) // 2)
    secondStageNewTime = random.randint(
        firstStageNewTime, (max_duration + min_duration) // 2
    )
    tasks[0] = [firstStageNewTime, secondStageNewTime]
    firstStageNewTime = random.randint(secondStageNewTime + 1, max_duration - 1)
    secondStageNewTime = random.randint(firstStageNewTime, max_duration)
    tasks[1] = [firstStageNewTime, secondStageNewTime]

    for i in range(2, len(tasks)):
        first_stage, second_stage = tasks[i]
        if first_stage > second_stage:
            break
        firstStageNewTime = random.randint(firstStageNewTime, max_duration - 1)
        if second_stage < firstStageNewTime:
            secondStageNewTime = random.randint(
                max(firstStageNewTime, secondStageNewTime), max_duration
            )
        else:
            secondStageNewTime = second_stage
        tasks[i] = [firstStageNewTime, secondStageNewTime]


def __generate_random_tasks(task_number, min_duration, max_duration):
    tasks = []

    # Создаем случайные задачи
    num_greater = random.randint(1, task_number - 2)
    num_less = random.randint(1, task_number - num_greater - 1)
    num_equal = task_number - num_greater - num_less

    # Где первый этап строго больше второго
    for _ in range(num_greater):
        stage1 = random.randint(min_duration + 1, max_duration)
        stage2 = random.randint(min_duration, stage1 - 1)
        tasks.append([stage1, stage2])

    # Где первый этап равен второму
    for _ in range(num_equal):
        stage1 = random.randint(min_duration, max_duration)
        stage2 = stage1
        tasks.append([stage1, stage2])

    # Где первый этап строго меньше второго
    for _ in range(num_less):
        stage1 = random.randint(min_duration, max_duration - 1)
        stage2 = random.randint(stage1 + 1, max_duration)
        tasks.append([stage1, stage2])

    return tasks


def generate_tasks(task_number, min_duration=1, max_duration=20):
    """
    Генератор условий для конвейерной задачи с гарантированным простоем.
    :param task_number: Количество задач.
    :param min_duration: Минимальная длительность одного этапа
    :param min_duration: Максимальная длительность одного этапа
    :return: Список заданий. Каждое задание - кортеж из двух чисел (длительность первого и второго этапа).
    """
    __validate_params(task_number, min_duration, max_duration)

    tasks = __generate_random_tasks(task_number, min_duration, max_duration)

    if not __has_downtime(tasks):
        __create_pseudorandom_in_start(tasks, min_duration, max_duration)

    random.shuffle(tasks)
    return tasks


def main(task_number: int, min_duration: int, max_duration: int) -> dict[str, Any]:
    return {TASKS: str(generate_tasks(task_number, min_duration, max_duration))}


if __name__ == "__main__":
    print(main(10, 10, 20))
