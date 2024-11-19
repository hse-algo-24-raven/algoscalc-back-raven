import importlib.util
import json
from typing import Callable

import pytest

from src.internal.algorithm_executor import AlgorithmExecutor
from src.internal.constants import (
    DEFAULT_DEFINITION_FILE_NAME,
    DEFAULT_FUNCTION_FILE_NAME,
    DEFAULT_TEST_FILE_NAME,
    DEFAULT_TIMEOUT,
)
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl
from src.internal.schemas.algorithm_definition_schema import AlgorithmDefinitionSchema
from src.internal.schemas.data_element_schema import DataElementSchema


class AlgorithmBuilder:
    """Класс создает экземпляры класса AlgorithmExecutor из пакетов с исходным кодом."""

    def __init__(
        self,
        definition_file_name: str = DEFAULT_DEFINITION_FILE_NAME,
        function_file_name: str = DEFAULT_FUNCTION_FILE_NAME,
        test_file_name: str = DEFAULT_TEST_FILE_NAME,
        execute_timeout: int = DEFAULT_TIMEOUT,
    ):
        """Конструктор класса

        :param definition_file_name: название файла с описанием алгоритма;
        :type definition_file_name: str
        :param function_file_name: название файла с методом для алгоритма;
        :type function_file_name: str
        :param test_file_name: название файла с тестами для метода алгоритма;
        :type test_file_name: str
        :param execute_timeout: таймаут выполнения алгоритма;
        :type execute_timeout: int
        :raises ValueError: при несоответствии типов данных для параметров.
        """
        self.__definition_file_name: str = definition_file_name
        self.__function_file_name: str = function_file_name
        self.__test_file_name: str = test_file_name
        self.__execute_timeout: int = execute_timeout
        self.__validate()

    def build_algorithm(self, path: str) -> AlgorithmExecutor:
        """Создает экземпляр класса AlgorithmExecutor на основе файлов с исходным
        кодом, расположенных в указанном каталоге.

        :param path: путь к каталогу с файлами исходного кода для алгоритма;
        :type path: str
        :return: экземпляр класса AlgorithmExecutor;
        :rtype: AlgorithmExecutor
        :raises ValueError: при несоответствии описания алгоритма;
        :raises RuntimeError: при ошибке выполнения авто тестов для алгоритма;
        :raises FileNotFoundError: при отсутствии файлов с исходным кодом;
        """
        with open(
            path + "/" + self.__definition_file_name, "r", encoding="utf-8"
        ) as def_file:
            definition_json = json.load(def_file)
        print(definition_json)
        algo_definition = AlgorithmDefinitionSchema.model_validate(definition_json)

        if not self.__test_function(path):
            raise RuntimeError(ErrMsg.UNIT_TEST_FAILED)

        return AlgorithmExecutor(
            algo_definition, self.__get_function(path), self.__execute_timeout
        )

    def __get_function(self, path: str) -> Callable:
        """Импортирует метод алгоритма из файла с исходным кодом."""
        file_name = self.__function_file_name
        spec = importlib.util.spec_from_file_location(file_name, path + "/" + file_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.main

    def __test_function(self, path: str) -> bool:
        """Выполняет тесты для алгоритма"""
        test_file_path = path + "/" + self.__test_file_name

        return pytest.main(["-q", test_file_path]) == 0

    def __validate(self) -> None:
        """Проверяет валидность созданного экземпляра класса."""
        if not isinstance(self.__execute_timeout, int) or isinstance(
            self.__execute_timeout, bool
        ):
            raise TypeError(ErrMsg.NON_INT_TIMEOUT)
        if self.__execute_timeout < 0:
            raise ValueError(ErrMsg.NEG_INT_TIMEOUT)
        str_params = [
            ["definition_file_name", self.__definition_file_name],
            ["function_file_name", self.__function_file_name],
            ["test_file_name", self.__test_file_name],
        ]
        for name, value in str_params:
            if not isinstance(value, str):
                raise TypeError(ErrMsgTmpl.NON_STRING_PARAM.format(name))
            if not value or not value.strip():
                raise ValueError(ErrMsgTmpl.EMPTY_STRING_PARAM.format(name))


if __name__ == "__main__":
    builder = AlgorithmBuilder(execute_timeout=0)
    algo_executor = builder.build_algorithm("src/algorithms/fibonacci")
    print(algo_executor.definition)
    print(algo_executor.execute([DataElementSchema(name="n", value=10)]))
