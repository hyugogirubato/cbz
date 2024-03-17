import secrets
import random
from datetime import datetime

import requests

from requests_toolbelt.multipart.encoder import MultipartEncoder


def fields(value: dict) -> dict:
    return {key: str(val) for key, val in value.items()}


def get_id() -> str:
    group1 = '-'.join([f'{random.randint(0, 255):02x}' for _ in range(6)])
    group2 = '-'.join([f'{random.randint(0, 255):02x}' for _ in range(6)])
    return f'{group1}:{group2}'


if __name__ == '__main__':
    database_table = 20  # Amazon
    device_token = secrets.token_hex(16)
    media_key_id = 'ac397b17ffaf4787af545de3035ca77c'
    device_id = get_id()
    user_email = 'example@mail.com'
    user_token = secrets.token_hex(16)
    device_platform = 49
    app_version = 6169
    user_subscription = 'register'
    media_id = 'B0CPPH5WK4'
    date = datetime.now().strftime('%Y-%m-%d')

    multipart_data = MultipartEncoder(
        fields({
            'IV': 100,
            'CM': 103,
            'TB': database_table,
            'KD': media_key_id,
            'MD': device_id,
            'EM': user_email,
            'PW': user_token,
            'CD': device_platform,
            'AV': app_version,
            'RT': user_subscription,
            'PD': media_id,
            'WD': 2,
            'LT': date
        })
    )

    # @Info: Cached keys
    r = requests.request(
        method='POST',
        url='https://drm-u1.dvdfab.cn/ak/uc/',
        data=multipart_data,
        headers={
            'Accept': '*/*',
            'Content-Type': multipart_data.content_type,
            'Expect': '100-continue',
            'User-Agent': 'DVDFab'
        }
    )
    r.raise_for_status()
    content = r.json()

    data = content['d']
    mod_key = content['k']
    unknown = content['u']  # TODO: ??
