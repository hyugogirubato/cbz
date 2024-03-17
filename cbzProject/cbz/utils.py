from enum import Enum


def dumps(data: dict) -> dict:
    return {k: v.value if isinstance(v, Enum) else v for k, v in data.items() if v and v != -1 and v != 'Unknown'}
