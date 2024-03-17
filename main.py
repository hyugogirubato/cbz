import requests
from pathlib import Path

from hidive.client import Client
from hidive.constants import Format, View
from hidive.utils import parse_pssh, b64encode

from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH

DEVICE = Path() / 'DEVICE.wvd'

if __name__ == '__main__':
    client = Client()
    client.login(email='EMAIL', password='PASSWORD')

    # @Info: series
    series = client.series(series_id=1049)
    print('[+] Series: %s' % series['title'])
    print('[+] Cover: %s' % series['coverUrl'])
    print('[+] Poster: %s' % series['posterUrl'])

    # @Info: seasons
    for view in series['seasons']:
        print('[+] Season: %s' % view['seasonNumber'])
        season = client.view(view=View.SEASON, view_id=view['id'])

        # @Info: episodes
        bucket = next(e for e in season['elements'] if e['$type'] == 'bucket')
        for episode in bucket['attributes']['items']:
            video_id = episode['id']
            print('[+] Title: %s' % episode['title'])
            print('[+] Description: %s' % episode['description'])

            details = client.details(video_id=video_id, playback=True)
            print('[+] Thumbnail: %s' % details['thumbnailUrl'])

            # @Info: subtitles
            playback = client.playback(url=details['playerUrlCallback'])
            dash = playback['dash'][0]
            for subtitle in dash['subtitles']:
                if subtitle['format'] == Format.VTT:
                    print('[+] Subtitle (%s): %s' % (subtitle['language'], subtitle['url']))

            # @Info: widevine DRM
            manifest_url = dash['url']
            print(f'[+] Manifest: {manifest_url}')
            assert 'WIDEVINE' in dash['drm']['keySystems'], 'Unsupported DRM system'

            manifest = requests.request(method='GET', url=manifest_url, headers={'User-Agent': Client.USER_AGENT}).text
            pssh = PSSH(parse_pssh(manifest))
            print(f'[+] PSSH: {pssh}')

            device = Device.load(DEVICE)
            cdm = Cdm.from_device(device)
            session_id = cdm.open()

            challenge = cdm.get_license_challenge(session_id, pssh)
            print('[+] Challenge: %s' % b64encode(challenge))

            licence = client.drm(
                url=dash['drm']['url'],
                token=dash['drm']['jwtToken'],
                key_ids=pssh.key_ids,
                challenge=challenge
            )
            print(f'[+] Licence: {b64encode(licence)}')

            cdm.parse_license(session_id, licence)
            keys = cdm.get_keys(session_id, type_='CONTENT')
            if not keys:
                raise ValueError('Could not find key')

            keys = [f'{k.kid.hex}:{k.key.hex()}' for k in keys]
            cdm.close(session_id)

            print('[+] Keys: %s' % '|'.join(keys))

            # @Info: download
            print('[+] Prompt: %s' % ' '.join([
                'N_m3u8DL-RE',
                f'"{manifest_url}"',
                *[f'--key "{k}"' for k in keys],
                '--header',
                f'"User-Agent: {Client.USER_AGENT}"'
            ]))
            exit(0)
