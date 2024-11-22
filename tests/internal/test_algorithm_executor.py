import time

import pytest

from src.internal.algorithm_executor import AlgorithmExecutor
from src.internal.constants import DEFAULT_TIMEOUT
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl
from src.internal.errors.exceptions import (
    AlgorithmTimeoutError,
    AlgorithmTypeError,
    AlgorithmUnexpectedError,
    AlgorithmValueError,
)
from src.internal.schemas.data_element_schema import DataElementSchema
from tests import NOT_INT_CASES, SCALAR_CASES, Case


def default_method(x):
    return {"y": x}


class TestAlgorithmExecutor:
    """Тесты для класса AlgorithmExecutor."""

    def test_valid_executor(self, create_algo_definition):
        """Проверяет создание валидного объекта с таймаутом по умолчанию"""
        algo_definition = create_algo_definition()

        algo_executor = AlgorithmExecutor(algo_definition, default_method)
        assert algo_executor.definition == algo_definition
        assert algo_executor.execute_timeout == DEFAULT_TIMEOUT

    def test_non_deterministic_executor(
        self, create_algo_definition, create_scalar_int_output_definition
    ):
        """Проверяет создание валидного объекта с не детерминированным
        элементом выходных данных"""
        algo_definition = create_algo_definition(
            outputs=[
                create_scalar_int_output_definition(
                    name="y", value=100500, is_deterministic=False
                )
            ]
        )

        algo_executor = AlgorithmExecutor(algo_definition, default_method)
        assert algo_executor.definition == algo_definition

    def test_set_timeout(self, create_algo_definition):
        """Проверяет создание валидного объекта с заданным таймаутом"""
        algo_definition = create_algo_definition()

        timeout = 1
        algo_executor = AlgorithmExecutor(algo_definition, default_method, timeout)
        assert algo_executor.definition == algo_definition
        assert algo_executor.execute_timeout == timeout

    @pytest.mark.parametrize(
        "test_case",
        NOT_INT_CASES,
        ids=[test_case.description for test_case in NOT_INT_CASES],
    )
    def test_not_int_execute_timeout(
        self,
        create_algo_definition,
        test_case: Case,
    ):
        """Проверяет ошибку указания не числового таймаута"""
        with pytest.raises(TypeError) as error:
            algo_definition = create_algo_definition()
            AlgorithmExecutor(algo_definition, default_method, test_case.value)
        assert str(error.value) == ErrMsg.NON_INT_TIMEOUT

    def test_negative_execute_timeout(self, create_algo_definition):
        """Проверяет ошибку указания отрицательного таймаута"""
        with pytest.raises(ValueError) as error:
            algo_definition = create_algo_definition()
            AlgorithmExecutor(algo_definition, default_method, -1)
        assert str(error.value) == ErrMsg.NEG_INT_TIMEOUT

    @pytest.mark.parametrize(
        "test_case",
        SCALAR_CASES,
        ids=[test_case.description for test_case in SCALAR_CASES],
    )
    def test_execute_method_not_callable(
        self,
        create_algo_definition,
        test_case: Case,
    ):
        """Проверяет ошибку указания некорректного метода"""
        with pytest.raises(TypeError) as error:
            AlgorithmExecutor(create_algo_definition(), test_case.value)
        assert str(error.value) == ErrMsg.METHOD_NOT_CALL

    def test_add_execute_method_timeout(self, create_algo_definition):
        """Проверяет прерывание исполнения по истечению таймаута"""
        algo_definition = create_algo_definition()
        timeout = 1

        def method(x):
            time.sleep(timeout + 1)
            return {"y": x}

        timeout_msg = ErrMsgTmpl.TIME_OVER.format(timeout, {"x": 1})

        with pytest.raises(RuntimeError) as error:
            AlgorithmExecutor(algo_definition, method, timeout)
        assert str(error.value) == ErrMsgTmpl.ADDING_METHOD_FAILED.format(timeout_msg)

    def test_zero_execute_timeout(self, create_algo_definition):
        """Проверяет отключение контроля времени выполнения
        при указании 0 таймаута"""
        algo_definition = create_algo_definition()
        timeout = 0

        def method(x):
            time.sleep(timeout + 1)
            return {"y": x}

        algo_executor = AlgorithmExecutor(algo_definition, method, timeout)
        assert algo_executor.execute_timeout == timeout
        assert algo_executor.execute([DataElementSchema(name="x", value=1)]) == [
            DataElementSchema(name="y", value=1)
        ]

    def test_add_execute_method_wrong_param(self, create_algo_definition):
        """Проверяет ошибку при указании метода с параметром не указанным
        в описании алгоритма"""
        algo_definition = create_algo_definition()

        def method(wrong_name):
            return {"y": wrong_name}

        err_msg = ErrMsgTmpl.ADDING_METHOD_FAILED.format(ErrMsg.UNEXPECTED_PARAM)
        with pytest.raises(RuntimeError) as error:
            AlgorithmExecutor(algo_definition, method)
        assert str(error.value) == err_msg

    def test_add_execute_method_missing_param(
        self,
        create_algo_definition,
        create_scalar_int_data_definition,
    ):
        """Проверяет ошибку при указании метода, в котором нет параметра,
        указанного в описании алгоритма"""
        algo_definition = create_algo_definition(
            parameters=[
                create_scalar_int_data_definition(name="x1"),
                create_scalar_int_data_definition(name="x2"),
            ]
        )

        def method(x1):
            return {"y": x1}

        err_msg = ErrMsgTmpl.ADDING_METHOD_FAILED.format(
            ErrMsg.UNEXPECTED_PARAM, {"x1": 1, "x2": 1}
        )
        with pytest.raises(RuntimeError) as error:
            AlgorithmExecutor(algo_definition, method)
        assert str(error.value) == err_msg

    def test_add_execute_method_wrong_output(self, create_algo_definition):
        """Проверяет ошибку при указании метода с выходными данными не указанными
        в описании алгоритма"""
        algo_definition = create_algo_definition()
        wrong_name = "wrong_name"

        def method(x):
            return {wrong_name: x}

        err_msg = ErrMsgTmpl.ADDING_METHOD_FAILED.format(
            ErrMsgTmpl.REDUNDANT_OUTPUT.format(wrong_name)
        )
        with pytest.raises(RuntimeError) as error:
            AlgorithmExecutor(algo_definition, method)
        assert str(error.value) == err_msg

    def test_add_execute_method_missing_output(
        self,
        create_algo_definition,
        create_scalar_int_output_definition,
    ):
        """Проверяет ошибку при указании метода, в котором нет одного из выходных
        данных, указанных в описании алгоритма"""
        algo_definition = create_algo_definition(
            outputs=[
                create_scalar_int_output_definition(name="y1"),
                create_scalar_int_output_definition(name="y2"),
            ]
        )

        def method(x):
            return {"y1": x}

        err_msg = ErrMsgTmpl.ADDING_METHOD_FAILED.format(
            ErrMsgTmpl.MISSED_OUTPUT.format("y2")
        )

        with pytest.raises(RuntimeError) as error:
            AlgorithmExecutor(algo_definition, method)
        assert str(error.value) == err_msg

    def test_add_execute_method_wrong_output_value(self, create_algo_definition):
        """Проверяет ошибку при указании метода, который не возвращает ожидаемого
        значения для дефолтных данных, указанных в описании алгоритма"""
        algo_definition = create_algo_definition()
        wrong_value = -1

        def method(x):
            return {"y": wrong_value}

        err_msg = ErrMsgTmpl.ADDING_METHOD_FAILED.format(
            ErrMsgTmpl.UNEXPECTED_OUTPUT.format(wrong_value, "y", 1)
        )
        with pytest.raises(RuntimeError) as error:
            AlgorithmExecutor(algo_definition, method)
        assert str(error.value) == err_msg

    def test_execute(
        self,
        create_algo_definition,
        create_scalar_int_data_definition,
        create_scalar_int_output_definition,
    ):
        """Проверяет выполнение алгоритма"""
        algo_definition = create_algo_definition(
            name="sum",
            parameters=[
                create_scalar_int_data_definition(name="a", value=1),
                create_scalar_int_data_definition(name="b", value=1),
            ],
            outputs=[create_scalar_int_output_definition(name="sum", value=2)],
        )

        def method(a, b):
            return {"sum": a + b}

        algo_executor = AlgorithmExecutor(algo_definition, method)
        params = [
            DataElementSchema(name="a", value=10),
            DataElementSchema(name="b", value=20),
        ]
        assert algo_executor.execute(params) == [
            DataElementSchema(name="sum", value=30)
        ]

    def test_execute_non_dict_params(self, create_algo_definition):
        """Проверяет ошибку выполнения алгоритма при передаче параметров
        в некорректном формате"""
        algo_definition = create_algo_definition()
        algo_executor = AlgorithmExecutor(algo_definition, default_method)

        with pytest.raises(AlgorithmTypeError) as error:
            algo_executor.execute(1)
        assert str(error.value) == ErrMsg.INCORRECT_PARAMS

    def test_execute_redundant_param(self, create_algo_definition):
        """Проверяет ошибку выполнения алгоритма при передаче лишнего параметра"""
        algo_definition = create_algo_definition()
        algo_executor = AlgorithmExecutor(algo_definition, default_method)

        redundant_param = "redundant_param"
        params = [
            DataElementSchema(name="x", value=1),
            DataElementSchema(name=redundant_param, value=1),
        ]

        with pytest.raises(AlgorithmValueError) as error:
            algo_executor.execute(params)
        assert str(error.value) == ErrMsgTmpl.REDUNDANT_PARAMETER.format(
            redundant_param
        )

    def test_execute_missed_param(
        self,
        create_algo_definition,
        create_scalar_int_data_definition,
        create_scalar_int_output_definition,
    ):
        """Проверяет ошибку выполнения алгоритма при отсутствии параметра"""
        algo_definition = create_algo_definition(
            name="sum",
            parameters=[
                create_scalar_int_data_definition(name="a", value=1),
                create_scalar_int_data_definition(name="b", value=1),
            ],
            outputs=[create_scalar_int_output_definition(name="sum", value=2)],
        )

        def method(a, b):
            return {"sum": a + b}

        algo_executor = AlgorithmExecutor(algo_definition, method)
        params = [DataElementSchema(name="a", value=1)]

        with pytest.raises(AlgorithmValueError) as error:
            algo_executor.execute(params)
        assert str(error.value) == ErrMsgTmpl.MISSED_PARAMETER.format("b")

    def test_execute_non_dict_output(self, create_algo_definition):
        """Проверяет ошибку выполнения алгоритма при выходнфх данных
        возвращенных не в формате словаря"""
        algo_definition = create_algo_definition()

        def method(x):
            return {"y": x} if x == 1 else x

        algo_executor = AlgorithmExecutor(algo_definition, method)
        params = [DataElementSchema(name="x", value=10)]

        with pytest.raises(AlgorithmTypeError) as error:
            algo_executor.execute(params)
        assert str(error.value) == ErrMsg.NOT_DICT_OUTPUTS

    def test_execute_timeout(self, create_algo_definition):
        """Проверяет прерывание выполнения алгоритма по истечению таймаута"""
        algo_definition = create_algo_definition()
        timeout = 1

        def method(x):
            time.sleep(x - 1)
            return {"y": x}

        algo_executor = AlgorithmExecutor(algo_definition, method, timeout)
        params = [DataElementSchema(name="x", value=timeout + 1)]

        with pytest.raises(AlgorithmTimeoutError) as error:
            algo_executor.execute(params)
        assert str(error.value) == ErrMsgTmpl.TIME_OVER.format(timeout, params)

    def test_execute_runtime_error(
        self, create_scalar_float_output_definition, create_algo_definition
    ):
        """Проверяет ошибку при выполнении алгоритма"""
        algo_definition = create_algo_definition(
            outputs=[create_scalar_float_output_definition(name="y")]
        )

        def method(x):
            return {"y": 1 / x}

        algo_executor = AlgorithmExecutor(algo_definition, method)
        params = [DataElementSchema(name="x", value=0)]

        with pytest.raises(AlgorithmUnexpectedError) as error:
            algo_executor.execute(params)
        assert str(error.value) == ErrMsg.UNEXPECTED_ERROR


if __name__ == "__main__":
    pytest.main(["-k", "TestAlgorithmExecutor"])
