import pytest

from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.schemas.algorithm_definition_schema import AlgorithmDefinitionSchema
from tests import (
    DESCRIPTION,
    NAME,
    OUTPUTS,
    PARAMETERS,
    SCALAR_CASES,
    TITLE,
    ErrorItemEnum,
)
from tests.internal.test_schemas.test_definition_schema import TestDefinitionSchema


class TestAlgorithmDefinitionSchema(TestDefinitionSchema):
    """Набор тестов для проверки класса описания алгоритма"""

    def test_valid_entity(
        self, create_scalar_int_data_definition, create_scalar_int_output_definition
    ):
        """Проверка создания объекта"""
        params = [create_scalar_int_data_definition(name="p")]
        outputs = [create_scalar_int_output_definition(name="o")]

        algo_definition = AlgorithmDefinitionSchema(
            name=NAME,
            title=TITLE,
            description=DESCRIPTION,
            parameters=params,
            outputs=outputs,
        )
        assert algo_definition.name == NAME
        assert algo_definition.title == TITLE
        assert algo_definition.description == DESCRIPTION
        assert algo_definition.parameters == params
        assert algo_definition.outputs == outputs

    def test_valid_entity_multiple_params(
        self, create_scalar_int_data_definition, create_scalar_int_output_definition
    ):
        """Проверка создания объекта с несколькими выходными данными"""
        params = [
            create_scalar_int_data_definition(name="p1"),
            create_scalar_int_data_definition(name="p2"),
        ]
        outputs = [create_scalar_int_output_definition(name="o")]

        algo_definition = AlgorithmDefinitionSchema(
            name=NAME,
            title=TITLE,
            description=DESCRIPTION,
            parameters=params,
            outputs=outputs,
        )
        assert algo_definition.parameters == params

    def test_valid_entity_multiple_outputs(
        self, create_scalar_int_data_definition, create_scalar_int_output_definition
    ):
        """Проверка создания объекта с несколькими входными параметрами"""
        params = [create_scalar_int_data_definition(name="p")]
        outputs = [
            create_scalar_int_output_definition(name="o1"),
            create_scalar_int_output_definition(name="o2"),
        ]

        algo_definition = AlgorithmDefinitionSchema(
            name=NAME,
            title=TITLE,
            description=DESCRIPTION,
            parameters=params,
            outputs=outputs,
        )
        assert algo_definition.outputs == outputs

    def test_immutable_entity(
        self, create_scalar_int_data_definition, create_scalar_int_output_definition
    ):
        """Проверка на неизменяемость объекта"""
        algo_definition = AlgorithmDefinitionSchema(
            name=NAME,
            title=TITLE,
            description=DESCRIPTION,
            parameters=[create_scalar_int_data_definition()],
            outputs=[create_scalar_int_output_definition()],
        )
        with pytest.raises(ValueError):
            algo_definition.name = "NewName"
        with pytest.raises(ValueError):
            algo_definition.title = "NewTitle"
        with pytest.raises(ValueError):
            algo_definition.description = "NewDescription"
        with pytest.raises(ValueError):
            algo_definition.parameters = [create_scalar_int_data_definition()]
        with pytest.raises(ValueError):
            algo_definition.outputs = [create_scalar_int_output_definition()]

    def test_empty_params(self, create_scalar_int_output_definition):
        """Ошибка отсутствия входных данных"""
        with pytest.raises(ValueError) as ctx:
            AlgorithmDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                parameters=[],
                outputs=[create_scalar_int_output_definition()],
            )
        assert len(ctx.value.errors()) == 1
        assert (
            ctx.value.errors()[0][ErrorItemEnum.MSG]
            == "Value error, " + ErrMsg.UNSET_PARAMS
        )

    def test_absent_params(self, create_scalar_int_output_definition):
        """Ошибка отсутствия входных данных"""
        with pytest.raises(ValueError) as ctx:
            AlgorithmDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                outputs=[create_scalar_int_output_definition()],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (PARAMETERS,)

    def test_absent_outputs(self, create_scalar_int_data_definition):
        """Ошибка отсутствия выходных данных"""
        with pytest.raises(ValueError) as ctx:
            AlgorithmDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                parameters=[create_scalar_int_data_definition()],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (OUTPUTS,)

    def test_duplicate_params(
        self, create_scalar_int_data_definition, create_scalar_int_output_definition
    ):
        """Ошибка дубликаты во входных данных"""
        with pytest.raises(ValueError) as ctx:
            AlgorithmDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                parameters=[
                    create_scalar_int_data_definition(),
                    create_scalar_int_data_definition(),
                ],
                outputs=[create_scalar_int_output_definition()],
            )
        assert len(ctx.value.errors()) == 1
        assert (
            ctx.value.errors()[0][ErrorItemEnum.MSG]
            == "Value error, " + ErrMsg.PARAMS_HAS_DUPLICATE
        )

    def test_duplicate_outputs(
        self, create_scalar_int_data_definition, create_scalar_int_output_definition
    ):
        """Ошибка дубликаты в выходных данных"""
        with pytest.raises(ValueError) as ctx:
            AlgorithmDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                parameters=[create_scalar_int_data_definition()],
                outputs=[
                    create_scalar_int_output_definition(),
                    create_scalar_int_output_definition(),
                ],
            )
        assert len(ctx.value.errors()) == 1
        assert (
            ctx.value.errors()[0][ErrorItemEnum.MSG]
            == "Value error, " + ErrMsg.OUTPUTS_HAS_DUPLICATE
        )

    @pytest.mark.parametrize(
        "test_case",
        SCALAR_CASES,
        ids=[test_case.description for test_case in SCALAR_CASES],
    )
    def test_invalid_params(self, create_scalar_int_output_definition, test_case):
        """Ошибка невалидные входные данных"""
        with pytest.raises(ValueError) as ctx:
            AlgorithmDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                parameters=test_case.value,
                outputs=[create_scalar_int_output_definition()],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (PARAMETERS,)

    @pytest.mark.parametrize(
        "test_case",
        SCALAR_CASES,
        ids=[test_case.description for test_case in SCALAR_CASES],
    )
    def test_invalid_in_params(
        self,
        create_scalar_int_data_definition,
        create_scalar_int_output_definition,
        test_case,
    ):
        """Ошибка невалидный элемент входных данных"""
        with pytest.raises(ValueError) as ctx:
            AlgorithmDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                parameters=[create_scalar_int_data_definition(), test_case.value],
                outputs=[create_scalar_int_output_definition()],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (PARAMETERS, 1)

    @pytest.mark.parametrize(
        "test_case",
        SCALAR_CASES,
        ids=[test_case.description for test_case in SCALAR_CASES],
    )
    def test_invalid_outputs(self, create_scalar_int_data_definition, test_case):
        """Ошибка невалидные выходные данных"""
        with pytest.raises(ValueError) as ctx:
            AlgorithmDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                parameters=[create_scalar_int_data_definition()],
                outputs=test_case.value,
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (OUTPUTS,)

    @pytest.mark.parametrize(
        "test_case",
        SCALAR_CASES,
        ids=[test_case.description for test_case in SCALAR_CASES],
    )
    def test_invalid_in_outputs(
        self,
        create_scalar_int_data_definition,
        create_scalar_int_output_definition,
        test_case,
    ):
        """Ошибка невалидный элемент выходных данных"""
        with pytest.raises(ValueError) as ctx:
            AlgorithmDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                parameters=[create_scalar_int_data_definition()],
                outputs=[create_scalar_int_output_definition(), test_case.value],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (OUTPUTS, 1)


if __name__ == "__main__":
    pytest.main(["-k", "TestAlgorithmDefinitionSchema"])
