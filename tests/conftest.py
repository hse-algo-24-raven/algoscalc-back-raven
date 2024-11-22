import json

import pytest

from src.internal.constants import (
    DEFAULT_DEFINITION_FILE_NAME,
    DEFAULT_FUNCTION_FILE_NAME,
    DEFAULT_TEST_FILE_NAME,
)
from src.internal.data_dimension.data_shape_enum import DataShapeEnum
from src.internal.data_dimension.data_type_enum import DataTypeEnum
from src.internal.schemas.algorithm_definition_schema import AlgorithmDefinitionSchema
from src.internal.schemas.data_definition_schema import DataDefinitionSchema
from src.internal.schemas.output_definition_schema import OutputDefinitionSchema
from tests import DESCRIPTION, FIB_DEF, FIB_FUNC, FIB_NAME, FIB_TESTS, NAME, TITLE


@pytest.fixture()
def tmp_algo_path(tmp_path):
    """Создает модуль для размещения алгоритмов"""
    init_file = tmp_path / "__init__.py"
    init_file.write_text(" ")
    return tmp_path


@pytest.fixture()
def fib_algo_dir(tmp_algo_path):
    """Создает модуль для алгоритма вычисления чисел Фибоначчи"""
    fib_dir = tmp_algo_path / FIB_NAME
    fib_dir.mkdir()
    init_file = fib_dir / "__init__.py"
    init_file.write_text(" ")
    def_file = fib_dir / DEFAULT_DEFINITION_FILE_NAME
    def_file.write_text(json.dumps(FIB_DEF), encoding="utf-8")
    func_file = fib_dir / DEFAULT_FUNCTION_FILE_NAME
    func_file.write_text(FIB_FUNC, encoding="utf-8")
    test_file = fib_dir / DEFAULT_TEST_FILE_NAME
    test_file.write_text(FIB_TESTS, encoding="utf-8")

    return str(fib_dir)


@pytest.fixture()
def algo_dir(tmp_algo_path):
    """Создает модуль для размещения заданного алгоритма"""

    def _algo_dir(dir_name, algo_def=None, algo_func=None, algo_test=None):
        algo_dir = tmp_algo_path / dir_name
        algo_dir.mkdir()
        init_file = algo_dir / "__init__.py"
        init_file.write_text(" ")
        if algo_def:
            def_file = algo_dir / DEFAULT_DEFINITION_FILE_NAME
            def_file.write_text(json.dumps(algo_def), encoding="utf-8")
        if algo_func:
            func_file = algo_dir / DEFAULT_FUNCTION_FILE_NAME
            func_file.write_text(algo_func, encoding="utf-8")
        if algo_test:
            test_file = algo_dir / DEFAULT_TEST_FILE_NAME
            test_file.write_text(algo_test, encoding="utf-8")

        return str(algo_dir)

    return _algo_dir


@pytest.fixture()
def create_scalar_int_data_definition():
    """Создает скалярное целочисленное описание данных"""

    def _create_scalar_int_data_definition(name=NAME, value=1):
        return DataDefinitionSchema(
            name=name,
            title="Data",
            description="Data description",
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.SCALAR,
            default_value=value,
        )

    return _create_scalar_int_data_definition


@pytest.fixture()
def create_scalar_float_output_definition():
    """Создает скалярное вещественное описание выходных данных"""

    def _create_scalar_float_output_definition(
        name=NAME, value=1, is_deterministic=True
    ):
        return OutputDefinitionSchema(
            name=name,
            title="Data",
            description="Data description",
            data_type=DataTypeEnum.FLOAT,
            data_shape=DataShapeEnum.SCALAR,
            default_value=value,
            is_deterministic=is_deterministic,
        )

    return _create_scalar_float_output_definition


@pytest.fixture()
def create_scalar_int_output_definition():
    """Создает скалярное целочисленное описание выходных данных"""

    def _create_scalar_int_output_definition(name=NAME, value=1, is_deterministic=True):
        return OutputDefinitionSchema(
            name=name,
            title="Data",
            description="Data description",
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.SCALAR,
            default_value=value,
            is_deterministic=is_deterministic,
        )

    return _create_scalar_int_output_definition


@pytest.fixture()
def create_scalar_float_data_definition():
    """Создает скалярное вещественное описание данных"""

    def _create_scalar_float_data_definition(name=NAME, value=1.0):
        return DataDefinitionSchema(
            name=name,
            title="Data",
            description="Data description",
            data_type=DataTypeEnum.FLOAT,
            data_shape=DataShapeEnum.SCALAR,
            default_value=value,
        )

    return _create_scalar_float_data_definition


@pytest.fixture()
def create_algo_definition(
    create_scalar_int_data_definition, create_scalar_int_output_definition
):
    """Создает описание алгоритма"""

    def _create_algo_definition(name=NAME, parameters=None, outputs=None):
        return AlgorithmDefinitionSchema(
            name=name,
            title=TITLE,
            description=DESCRIPTION,
            parameters=parameters or [create_scalar_int_data_definition("x")],
            outputs=outputs or [create_scalar_int_output_definition("y")],
        )

    return _create_algo_definition
