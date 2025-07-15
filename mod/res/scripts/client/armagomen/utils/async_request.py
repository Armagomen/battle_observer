import json

import BigWorld

from wg_async import AsyncReturn, await_callback, wg_async

REQUEST_TIMEOUT = 15.0
DEFAULT_HEADERS = {"User-Agent": "Battle-Observer-App", "Content-Type": "application/json"}


@wg_async
def async_url_request(url, data=None, headers=None, method='GET'):
    final_headers = DEFAULT_HEADERS.copy()
    if headers:
        final_headers.update(headers)
    postData = json.dumps(data or {}) if method in ['POST', 'PATCH'] else ''
    response = yield await_callback(_internal_fetch)(url, final_headers.items(), method, postData)
    raise AsyncReturn(response)


def _internal_fetch(url, headers, method, postData, callback=lambda x: x):
    return BigWorld.fetchURL(url, callback, headers, REQUEST_TIMEOUT, method, postData)
