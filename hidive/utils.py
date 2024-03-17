import base64
import json
import re
import time
from typing import Union


def b64decode(value: str) -> bytes:
    return base64.b64decode(value + '=' * (4 - len(value) % 4))


def b64encode(value: Union[str, bytes, dict, list]) -> str:
    if isinstance(value, (dict, list)):
        value = json.dumps(value, separators=(',', ':'))
    if isinstance(value, str):
        value = value.encode('utf-8')
    return base64.b64encode(value).decode('utf-8')


def jwt_expired(value: str) -> bool:
    header, payload, signature = value.split('.', 2)
    payload = json.loads(b64decode(payload))
    return payload['exp'] < round(time.time())


def parse_pssh(value: str) -> str:
    lines = value.splitlines()
    for i, line in enumerate(lines):
        if 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed' in line:
            return re.search(r'<cenc:pssh>(.+)</cenc:pssh>', lines[i + 1]).group(1)
    raise ValueError('Could not find pssh')
