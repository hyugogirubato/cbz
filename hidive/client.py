import time
from urllib.parse import urlencode
from uuid import UUID

import requests
from requests import Response

from hidive.constants import View, Filter
from hidive.utils import jwt_expired, b64encode


class Client:
    USER_AGENT = 'ExoDoris/2.2.7 (Linux;Android 10) AndroidXMedia3/1.0.2'

    def __init__(self, access_token: str = None, refresh_token: str = None):
        self.api = 'https://dce-frontoffice.imggaming.com/api'
        self.guide = 'https://guide.imggaming.com'
        self.algolia = 'https://h99xldr8mj-dsn.algolia.net'
        self.user = {
            'authorisationToken': access_token or '',
            'refreshToken': refresh_token or ''
        }

    def __request(self, **kwargs) -> Response:
        headers = {
            'Accept': '*/*',
            'User-Agent': 'okhttp/4.9.2',
            **kwargs.get('headers', {})
        }

        url: str = kwargs.get('url')
        params = kwargs.get('params', {})

        if url.startswith(self.api) or url.startswith(self.guide):
            headers['app'] = 'dice'
            headers['realm'] = 'dce.hidive'
            headers['x-api-key'] = '4dc1e8df-5869-41ea-95c2-6f04c67459ed'
            headers['x-app-var'] = '2.2.7'

            if kwargs.get('auth', True):
                headers['Authorization'] = self.__token()
        elif url.startswith(self.algolia):
            params['x-algolia-agent'] = 'Algolia for JavaScript (3.35.1); React Native'
            params['x-algolia-application-id'] = 'H99XLDR8MJ'
            params['x-algolia-api-key'] = 'e55ccb3db0399eabe2bfc37a0314c346'

        r = requests.request(
            method=kwargs.get('method', 'GET'),
            url=url,
            params=params,
            json=kwargs.get('json'),
            data=kwargs.get('data'),
            headers=headers
        )
        r.raise_for_status()
        return r

    def __token(self) -> str:
        access_token = self.user.get('authorisationToken')
        if not access_token:
            self.guest()
        elif jwt_expired(access_token):
            self.refresh()
        return 'Bearer %s' % self.user['authorisationToken']

    # @package: login
    def guest(self) -> dict:
        content = self.__request(method='POST', url=f'{self.api}/v2/login/guest/checkin', auth=False).json()
        self.user.update(content)
        return content

    def refresh(self) -> dict:
        refresh_token = self.user['refreshToken']
        if jwt_expired(refresh_token):
            raise ValueError('Refresh token expired')

        content = self.__request(
            method='POST',
            url=f'{self.api}/v2/token/refresh',
            json={'refreshToken': refresh_token}
        ).json()
        self.user.update(content)
        return content

    def login(self, email: str, password: str) -> dict:
        content = self.__request(
            method='POST',
            url=f'{self.api}/v2/login',
            json={'id': email, 'secret': password}
        ).json()
        self.user.update(content)
        return content

    def reset(self, email: str) -> dict:
        return self.__request(
            method='POST',
            url=f'{self.api}/v2/reset-password/create',
            json={'id': email, 'provider': 'ID'},
            auth=False
        ).json()

    def create(self, email: str, password: str) -> dict:
        content = self.__request(
            method='POST',
            url=f'{self.api}/v2/user',
            json={
                'email': email,
                'secret': password,
                'consentAnswers': [{
                    'answer': f['required'],
                    'promptField': f['fieldName']
                } for f in self.consent()['fields']]
            }
        ).json()
        self.user.update(content)
        return content

    # @package: realm
    def providers(self) -> list[dict]:
        return self.__request(
            method='GET',
            url=f'{self.api}/v2/realm/authentication-providers'
        ).json()['authenticationProviders']

    def settings(self) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v2/realm-settings/realm/dce.hidive').json()

    def label(self) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v2/label/dce.hidive').json()

    def licence(self) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v2/licence').json()

    def consent(self) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v2/consent-prompt').json()

    # @package: user
    def preferences(self, auto_play: bool = None) -> dict:
        method = 'GET' if auto_play is None else 'PUT'
        data = None if auto_play is None else {'autoAdvance': auto_play}
        return self.__request(method=method, url=f'{self.api}/v2/user/preferences', json=data).json()

    def profile(self) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v2/user/profile').json()

    def notification(self, limit: int = 1) -> dict:
        return self.__request(
            method='GET',
            url=f'{self.api}/v2/promo-notification',
            params={'maxNotifications': limit}
        ).json()

    def watch_create(self, name: str) -> dict:
        return self.__request(
            method='POST',
            url=f'{self.api}/v3/user/watchlist',
            json={'name': name}
        ).json()

    def watch_delete(self, watch_id: int) -> None:
        href = b64encode('480211|dce.hidive')
        self.__request(method='DELETE', url=f'{self.api}/v3/user/watchlist/{href}/{watch_id}')

    def watch(self, limit: int = 25) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v3/user/watchlist', params={'rpp': limit}).json()

    def watch_add(self, watch_id: int, content_type: str, content_id: int) -> dict:
        return self.__request(
            method='POST',
            url=f'{self.api}/v4/user/watchlist/{watch_id}/content',
            json={'content': [{'contentType': content_type, 'id': content_id}]}
        ).json()

    def watch_remove(self, watch_id: int, content_type: str, content_id: int) -> None:
        self.__request(
            method='DELETE',
            url=f'{self.api}/v4/user/watchlist/{watch_id}/content/{content_type}/{content_id}'
        )

    def watch_details(self, watch_id: int, limit: int = 25) -> dict:
        return self.__request(
            method='GET',
            url=f'{self.api}/v4/user/watchlist/{watch_id}',
            params={'rpp': limit}
        ).json()

    # @package: content
    def menu(self) -> list[dict]:
        return self.__request(method='GET', url=f'{self.api}/v2/menu-items').json()

    def event(self, limit: int = 20) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v2/event/live', params={'rpp': limit}).json()

    def content(self, title: str = 'home') -> dict:
        # @Default: home | browse
        return self.__request(
            method='GET',
            url=f'{self.api}/v4/content/{title}',
            params={
                'bpp': 10,
                'rpp': 12,
                'displaySectionLinkBuckets': 'SHOW',
                'displayEpgBuckets': 'SHOW',
                'displayEmptyBucketShortcuts': 'SHOW',
                'displayGeoblocked': 'SHOW',
                'bspp': 20
            }
        ).json()

    def popular(self) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v2/popular').json()

    def view(self, view: View, view_id: int) -> dict:
        return self.__request(
            method='GET',
            url=f'{self.api}/v1/view',
            params={'type': view.value, 'id': view_id}
        ).json()

    def series(self, series_id: int, limit: int = 1) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v4/series/{series_id}', params={'rpp': limit}).json()

    def query(
            self,
            query: str,
            facets: list = None,
            facet_filters: list = None,
            page: int = 0,
            filters: Filter = None
    ) -> dict:
        params = {
            'facets': facets or [],
            'query': query,
            'facetFilters': facet_filters or []
        }
        if filters:
            params['filters'] = f'type:{filters.value}'
        else:
            params['page'] = page

        return self.__request(
            method='POST',
            url=f'{self.algolia}/1/indexes/prod-dce.hidive-livestreaming-events/query',
            json={'params': urlencode(params)}
        ).json()

    # @package: vod
    def live(self, video_id: int) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v4/vods/live/{video_id}').json()

    def stream(self, video_id: int) -> dict:
        return self.__request(method='GET', url=f'{self.api}/v3/stream/vod/{video_id}').json()

    def details(self, video_id: int, playback: bool = True) -> dict:
        return self.__request(
            method='GET',
            url=f'{self.api}/v2/vod/{video_id}',
            params={'includePlaybackDetails': 'URL'} if playback else None,
            headers={
                'cm-app-bundle': 'com.hidive.android',
                'cm-app-name': 'HIDIVE',
                'cm-app-storeid': 'com.hidive.android',
                'cm-app-version': '2.2.7',
                'cm-cst-ifa': '',
                'cm-cst-lat': '0',
                'cm-cst-tcf': '',
                'cm-cst-usp': '',
                'cm-dvc-dnt': '0',
                'cm-dvc-h': '720',
                'cm-dvc-lang': 'en_US',
                'cm-dvc-make': 'Xiaomi',
                'cm-dvc-model': 'Mi A2',
                'cm-dvc-os': '2',
                'cm-dvc-osv': '10',
                'cm-dvc-type': '4',
                'cm-dvc-w': '360'
            }
        ).json()

    def adjacent(self, video_id: int, limit: int = 20) -> dict:
        return self.__request(
            method='GET',
            url=f'{self.api}/v4/vod/{video_id}/adjacent',
            params={'size': limit}
        ).json()

    # @package: player
    def progress(self, video_id: int, cid: str, progress: int) -> dict:
        return self.__request(
            method='PUT',
            url=f'{self.guide}/prod',
            params={
                'action': 2,
                'cid': cid,
                'nature': 'last',
                'progress': progress,
                'startedAt': round(time.time()),
                'video': video_id
            }
        ).json()

    def playback(self, url: str) -> dict:
        return self.__request(method='GET', url=url, auth=False).json()

    def drm(self, url: str, token: str, key_ids: list[UUID], challenge: bytes) -> bytes:
        # @Info: widevine DRM
        return self.__request(
            method='POST',
            url=url,
            data=challenge,
            headers={
                'Authorization': f'Bearer {token}',
                'User-Agent': 'Dice Shield/2.2.7 (Linux;Android 10) AndroidXMedia3/1.0.2',
                'X-DRM-INFO': b64encode({
                    'system': 'com.widevine.alpha',
                    'key_ids': [str(k) for k in key_ids]
                })
            }
        ).content
