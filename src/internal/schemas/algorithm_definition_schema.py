from typing import Self

from pydantic import ConfigDict, model_validator

from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.schemas.data_definition_schema import DataDefinitionSchema
from src.internal.schemas.definition_schema import DefinitionSchema
from src.internal.schemas.output_definition_schema import OutputDefinitionSchema


class AlgorithmDefinitionSchema(DefinitionSchema):
    """Класс представляет описание алгоритма, структуры его входных и
    выходных данных."""

    model_config = ConfigDict(frozen=True)

    parameters: list[DataDefinitionSchema]
    outputs: list[OutputDefinitionSchema]

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра класса."""
        return f'AlgorithmDefinition: {self.name}, "{self.title}"'

    @model_validator(mode="after")
    def check_unique(self) -> Self:
        """Проверяет что входные и выходные данные заданы и в них нет
        дубликатов по названию"""
        if len(self.parameters) == 0:
            raise ValueError(ErrMsg.UNSET_PARAMS)
        param_names = [param.name for param in self.parameters]
        if len(param_names) != len(set(param_names)):
            raise ValueError(ErrMsg.PARAMS_HAS_DUPLICATE)

        if len(self.outputs) == 0:
            raise ValueError(ErrMsg.UNSET_OUTPUTS)
        output_names = [output.name for output in self.outputs]
        if len(output_names) != len(set(output_names)):
            raise ValueError(ErrMsg.OUTPUTS_HAS_DUPLICATE)
        return self


if __name__ == "__main__":
    algorithm_definition = AlgorithmDefinitionSchema(
        name="alg",
        title="Algorithm",
        description="Some description",
        parameters=[
            DataDefinitionSchema(
                name="p",
                title="Param",
                description="Param description",
                data_type="INT",
                data_shape="SCALAR",
                default_value=1,
            )
        ],
        outputs=[
            OutputDefinitionSchema(
                name="O",
                title="Output",
                description="Output description",
                data_type="INT",
                data_shape="SCALAR",
                default_value=1,
            )
        ],
    )
    print(algorithm_definition.model_dump())
