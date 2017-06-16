import binascii
from base64 import b64decode

from aiohttp import ClientResponseError, ClientSession
from requests import get


def decode_dict(d):
    """
    Recursivly decode all strings in a dict
    :param d: the input dict
    :return: a dict with all its vals decoded
    """
    if isinstance(d, int):
        return d
    elif isinstance(d, str):
        return __decode(d)
    elif isinstance(d, list):
        return [decode_dict(s) for s in d]
    elif isinstance(d, dict):
        return {k: decode_dict(v) for k, v in d.items()}


def __decode(s: str):
    """
    Deconde a base64 string into utf8
    :param s: the base64 encoded string
    :return: the utf-8 decoded string
    """
    try:
        return b64decode(s).decode('utf-8')
    except binascii.Error:
        return s


def get_token():
    """
    Get a session token
    :return: a session token
    """
    return get(
        'https://opentdb.com/api_token.php?command=request').json()['token']


async def make_request(session: ClientSession, url):
    async with session.get(url) as r:
        if r.status != 200:
            raise ClientResponseError
        return r
