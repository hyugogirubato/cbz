import json
import re
from pathlib import Path

import requests

PARENT = Path()


def sanitize(value: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', value)


if __name__ == '__main__':
    avatar = json.loads((PARENT / 'avatar.json').read_bytes())
    for item in avatar['items']:
        path = PARENT / 'Avatar' / sanitize(item['title'])
        path.mkdir(parents=True, exist_ok=True)
        for asset in item['assets']:
            url = 'https://static.crunchyroll.com/assets/avatar/170x170/' + asset['id']
            r = requests.request(
                method='GET',
                url=url,
                headers={
                    'Accept': '*/*',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; Mi A2 Build/QKQ1.190910.002)'
                }
            )
            r.raise_for_status()

            file = path / sanitize(asset['id'])
            file.write_bytes(r.content)
            print(file)
