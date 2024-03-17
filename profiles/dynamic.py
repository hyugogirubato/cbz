import secrets
import random

import requests

from requests_toolbelt.multipart.encoder import MultipartEncoder


def fields(value: dict) -> dict:
    return {key: str(val) for key, val in value.items()}


def get_id() -> str:
    group1 = '-'.join([f'{random.randint(0, 255):02x}' for _ in range(6)])
    group2 = '-'.join([f'{random.randint(0, 255):02x}' for _ in range(6)])
    return f'{group1}:{group2}'


if __name__ == '__main__':
    user_email = 'example@mail.com'
    user_token = secrets.token_hex(16)
    user_subscription = 'register'
    device_token = secrets.token_hex(16)
    device_platform = 49
    device_id = get_id()
    app_version = 6169
    media_id = 'B0CPPH5WK4'
    pssh = 'CAESEM235gyo/kFAk//K99EUxOAaBmFtYXpvbiI1Y2lkOnpiZm1ES2orUVVDVC84cjMwUlRFNEE9PSxRWVJUWXJnd1JxbXBzMngvTnM0alVRPT0qAlNEMgA='
    certificate = 'CAUSwgUKvAIIAxIQCuQRtZRasVgFt7DIvVtVHBi17OSpBSKOAjCCAQoCggEBAKU2UrYVOSDlcXajWhpEgGhqGraJtFdUPgu6plJGy9ViaRn5mhyXON5PXmw1krQdi0SLxf00FfIgnYFLpDfvNeItGn9rcx0RNPwP39PW7aW0Fbqi6VCaKWlR24kRpd7NQ4woyMXr7xlBWPwPNxK4xmR/6UuvKyYWEkroyeIjWHAqgCjCmpfIpVcPsyrnMuPFGl82MMVnAhTweTKnEPOqJpxQ1bdQvVNCvkba5gjOTbEnJ7aXegwhmCdRQzXjTeEV2dO8oo5YfxW6pRBovzF6wYBMQYpSCJIA24ptAP/2TkneyJuqm4hJNFvtF8fsBgTQQ4TIhnX4bZ9imuhivYLa6HsCAwEAAToPYW1hem9uLmNvbS1wcm9kEoADETQD6R0H/h9fyg0Hw7mj0M7T4s0bcBf4fMhARpwk2X4HpvB49bJ5Yvc4t41mAnXGe/wiXbzsddKMiMffkSE1QWK1CFPBgziU23y1PjQToGiIv/sJIFRKRJ4qMBxIl95xlvSEzKdt68n7wqGa442+uAgk7CXU3uTfVofYY76CrPBnEKQfad/CVqTh48geNTb4qRH1TX30NzCsB9NWlcdvg10pCnWSm8cSHu1d9yH+2yQgsGe52QoHHCqHNzG/wAxMYWTevXQW7EPTBeFySPY0xUN+2F2FhCf5/A7uFUHywd0zNTswh0QJc93LBTh46clRLO+d4RKBiBSj3rah6Y5iXMw9N9o58tCRc9gFHrjfMNubopWHjDOO3ATUgqXrTp+fKVCmsGuGl1ComHxXV9i1AqHwzzY2JY2vFqo73jR3IElr6oChPIwcNokmNc0D4TXtjE0BoYkbWKJfHvJJihzMOvDicWUsemVHvua9/FBtpbHgpbgwijFPjtQF9Ldb8Swf'

    multipart_data = MultipartEncoder(
        fields({
            'T': 10,
            'B': 6,
            'C': user_email,
            'D': user_token,
            'E': user_subscription,
            'F': device_token,
            'G': device_platform,
            'H': device_id,
            'I': 1,
            'Z': app_version,
            'K': 2,
            'L': media_id,
            'M': pssh,
            'N': certificate
        })
    )

    # @Info: Challenge
    r = requests.request(
        method='POST',
        url='https://drm-w-j2.dvdfab.cn/ex/',
        data=multipart_data,
        headers={
            'Accept': '*/*',
            'Content-Type': multipart_data.content_type,
            'Expect': '100-continue',
            'User-Agent': 'DVDFab'
        }
    )
    r.raise_for_status()

    challenge = r.json()['FB']
    print(f'[+] Challenge: {challenge}')

    licence = ''  # TODO: AMZ License

    # @Info: Keys
    multipart_data = MultipartEncoder(
        fields({
            'T': 12,
            'B': 6,
            'C': email,
            'D': user_token,
            'E': user_subscription,
            'F': device_token,
            'G': device_platform,
            'H': device_id,
            'I': 1,
            'Z': app_version,
            'K': 2,
            'L': media_id,
            'M': pssh,
            'N': certificate,
            'O': licence
        })
    )

    r = requests.request(
        method='POST',
        url='https://drm-w-j2.dvdfab.cn/ex/',
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

    data = content['D']
    mod_key = content['T']
