from sbin import BaseModel, dump2file


class Model(BaseModel):
    """
    Create a model (schema) that will be used by the dump2file function to actually serialize the dictionary.
    Any kind of typed dict may be used instead of the BaseModel
    """

    x: int
    y: int
    k: float


"""
dump2file accepts a list of dicts of the type BaseModel.
Alternatively it also accepts a single dictionary.
Look at the dump2file documentation for more information..
"""
test_list = [{"x": 12, "y": 20, "k": 12.0}, {"x": 20, "y": 9, "k": 25}]

dump2file("test1.bin", Model, test_list)

test_one = {"x": 5, "y": 55, "k": 2.0}

dump2file("test2.bin", Model, test_one)
