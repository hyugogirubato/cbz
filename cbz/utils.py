from enum import Enum
from typing import Any


def dumps(data: dict) -> dict:
    return {k: v.value if isinstance(v, Enum) else v for k, v in data.items() if v and v != -1 and v != 'Unknown'}


def _check_type(key: str, value: Any, types: tuple) -> Any:
    """
    Check type of value, and cast this value to first type of the types
    :param key: name of key of variable (using only for best error information)
    :param value: value for a check
    :param types: list of the allowed types
    :return: value with new type
    """
    if not isinstance(value, types):
        raise ValueError(
            f"Unexpected type of {key}, got: {type(value).__name__}, expected: {[i.__name__ for i in types]}")
    return types[0](value)


def _get(obj: Any, fields: tuple) -> dict:
    """
    Create dictionary from variables by PAGE_FIELDS
    :return: dictionary with variables value
    """
    return {key[1]: _check_type(value[0], getattr(obj, value[0]), value[1]) for key, value in fields}


def _set(obj: Any, fields: tuple, data_dict: dict) -> None:
    """
    Set class variables from input dictionary, check types of input and cast values to correct type
    :param kwargs: dictionary of input data
    """
    for kwarg_key, kwarg_value in data_dict.items():
        for keys, values in fields:
            if kwarg_key in keys:
                variable, types = values
                if hasattr(obj, variable):
                    setattr(obj, variable, _check_type(kwarg_key, kwarg_value, types))
                    break
