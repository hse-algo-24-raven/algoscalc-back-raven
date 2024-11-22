import pytest

from src.internal.data_dimension.data_shape_enum import DataShapeEnum
from src.internal.data_dimension.data_type_enum import DataTypeEnum
from src.internal.schemas.output_definition_schema import OutputDefinitionSchema
from tests import BOOL_CASES, DESCRIPTION, NAME, TITLE
from tests.internal.test_schemas.test_data_definition_schema import (
    TestDataDefinitionSchema,
)


class TestOutputDefinitionSchema(TestDataDefinitionSchema):
    """Набор тестов для проверки класса OutputDefinitionSchema"""

    @pytest.mark.parametrize(
        "test_case",
        BOOL_CASES,
    )
    def test_valid_entity(self, test_case):
        """Проверка создания объекта"""
        data_definition = OutputDefinitionSchema(
            name=NAME,
            title=TITLE,
            description=DESCRIPTION,
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.SCALAR,
            default_value=1,
            is_deterministic=test_case.value,
        )
        assert data_definition.name == NAME
        assert data_definition.title == TITLE
        assert data_definition.description == DESCRIPTION
        assert data_definition.data_type == DataTypeEnum.INT
        assert data_definition.data_shape == DataShapeEnum.SCALAR
        assert data_definition.default_value == 1
        assert data_definition.is_deterministic == test_case.value

    def test_valid_entity_default_deterministic(self):
        """Проверка создания объекта со значением по умолчанию для is_deterministic"""
        data_definition = OutputDefinitionSchema(
            name=NAME,
            title=TITLE,
            description=DESCRIPTION,
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.SCALAR,
            default_value=1,
        )
        assert data_definition.is_deterministic


if __name__ == "__main__":
    pytest.main(["-k", "TestOutputDefinitionSchema"])
