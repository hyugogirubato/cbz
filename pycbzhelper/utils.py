from __future__ import annotations
from typing import Union

import unicodedata


def get_key_value(value: Union[str, bool]) -> str:
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return value


def delete_none(_dict: dict) -> dict:
    """Delete None values recursively from all of the dictionaries, tuples, lists, sets"""
    if isinstance(_dict, dict):
        for key, value in list(_dict.items()):
            if isinstance(value, (list, dict, tuple, set)):
                _dict[key] = delete_none(value)
            elif value is None or key is None:
                del _dict[key]
            if value == {}:
                del _dict[key]

    elif isinstance(_dict, (list, set, tuple)):
        _dict = type(_dict)(delete_none(item) for item in _dict if item is not None)
    return _dict


def slugify(value: Union[str, int], allow_unicode: bool = False) -> str:
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    # value = re.sub(r'[^\w\s-]', '', value.lower())
    # return re.sub(r'[-\s]+', '-', value).strip('-_')
    return value
