"""
"""

from functools import reduce

from panda3d_toolbox import text

def set_setters_from_dict(obj: object, data: dict) -> None:
    """
    Sets the attributes of an object from a dictionary. 
    The dictionary keys should match the object's setter methods.

    IE. name -> set_name(self, name)
    """

    for key, values in data.items():
        setter = f"set_{text.get_snake_case(key)}"
        if not hasattr(obj, setter):
            raise AttributeError(
                f"Object {obj} does not have a setter for {key}")

        if not isinstance(values, list):
            values = [values]

        getattr(obj, setter)(*values)

def has_attributes(object: object, attributes: list) -> list:
    """
    """

    return reduce(bool.__and__, [ hasattr(object, attr) for attr in attributes ])

def is_awaitable_function(func: object) -> bool:
    """
    Returns true if the function is awaitable
    """

    assert func != None
    assert callable(func)

    import inspect
    return inspect.iscoroutinefunction(func)