from typing import TypedDict, Union
import struct
from os.path import exists


BaseModel = TypedDict


def create_header(model: BaseModel) -> str:
    header = "<!"
    for key, value in model.__annotations__.items():
        header += f"{key}: "
        header += value.__name__ + ", "
    header = header[:-2] + ">"
    return header


def create_schema(model: BaseModel) -> str:
    schema = "<"
    for value in model.__annotations__.values():
        if value.__name__ == "int":
            schema += "i"
        elif value.__name__ == "float":
            schema += "f"
        else:
            raise AssertionError("No valid data types were provided!")
    return schema


def map_annotations_to_data(model: BaseModel, data: dict) -> list[any]:
    output = []
    for value in model.__annotations__.keys():
        output.append(data[value])
    return output


def dump2file(
    filename: str,
    model: BaseModel,
    data: Union[list[BaseModel], BaseModel],
    append=False,
):
    """
    > filename: Name of the file to be saved.
    > model: Class of the BaseModel (TypedDict) type.
    > data: A list of dicts of the type of the model or a single dict.
    > append: Save the content in a existing file without overwriting it's contents. Default: false.
        >> A header will not be created in the file even if the file is empty.
        >> If the file doesn't exist it will be created
    """

    if append and exists(filename):
        with open(filename, "ba") as file:
            schema = create_schema(model)
            if isinstance(data, list):
                for el in data:
                    if el.keys() == model.__required_keys__:
                        packed = struct.pack(
                            schema, *map_annotations_to_data(model, el)
                        )
                        file.write(packed)
                    else:
                        raise KeyError(
                            "The data provided does not match the model schema!"
                        )
            elif isinstance(data, BaseModel):
                if data.keys() == model.__required_keys__:
                    packed = struct.pack(schema, *map_annotations_to_data(model, data))
                    file.write(packed)
                else:
                    raise KeyError("The data provided does not match the model schema!")
            else:
                raise AssertionError("No valid data types were provided!")
    else:
        with open(filename, "bw") as file:
            file.write(create_header(model).encode())
            schema = create_schema(model)
            if isinstance(data, list):
                for el in data:
                    if el.keys() == model.__required_keys__:
                        packed = struct.pack(
                            schema, *map_annotations_to_data(model, el)
                        )
                        file.write(packed)
                    else:
                        raise KeyError(
                            "The data provided does not match the model schema!"
                        )
            elif isinstance(data, dict):
                if data.keys() == model.__required_keys__:
                    packed = struct.pack(schema, *map_annotations_to_data(model, data))
                    file.write(packed)
                else:
                    raise KeyError("The data provided does not match the model schema!")
            else:
                raise AssertionError("No valid data types were provided!")
