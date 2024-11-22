from src.internal.data_dimension.data_shape_enum import DataShapeEnum
from src.internal.data_dimension.data_type_enum import DataTypeEnum
from src.internal.schemas.data_definition_schema import DataDefinitionSchema


class OutputDefinitionSchema(DataDefinitionSchema):
    """Класс представляет описание элемента выходных данных алгоритма.

    Выходные данные некоторых алгоритмов не могут быть определены заранее
    и протестированы при сборке алгоритма в данном случае устанавливается
    флаг is_deterministic=False."""

    is_deterministic: bool = True


if __name__ == "__main__":
    non_deterministic_data = OutputDefinitionSchema(
        name="data",
        title="Data",
        description="Input data",
        data_type=DataTypeEnum.INT,
        data_shape=DataShapeEnum.SCALAR,
        is_deterministic=False,
        default_value=1,
    )
    print(non_deterministic_data.model_dump)
