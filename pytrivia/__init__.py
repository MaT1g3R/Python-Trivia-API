"""
A simple python api wrapper for https://opentdb.com/
"""
import binascii
from base64 import b64decode
from enum import Enum
from json import loads

from requests import get


class Category(Enum):
    General = 9
    Books = 10
    Film = 11
    Music = 12
    Musicals_Theatres = 13
    Tv = 14
    Video_Games = 15
    Board_Games = 16
    Nature = 17
    Computers = 18
    Maths = 19
    Mythology = 20
    Sports = 21
    Geography = 22
    History = 23
    Politics = 24
    Art = 25
    Celebrities = 26
    Animals = 27
    Vehicles = 28
    Comics = 29
    Gadgets = 30
    Anime_Manga = 31
    Cartoon = 32


class Diffculty(Enum):
    Easy = 'easy'
    Medium = 'medium'
    Hard = 'hard'


class Type(Enum):
    Multiple_Choice = 'multiple'
    True_False = 'boolean'


class Trivia:
    def __init__(self, with_token: bool):
        """
        Initialize an instance of the Trivia class
        :param with_token: If True then the instance will uses a session token
        """
        self.token = _get_token() if with_token else None

    def request(self, num_questions: int, category: Category = None,
                diffculty: Diffculty = None, type_: Type = None):
        """
        Send an api request to https://opentdb.com/
        Limitations:
        Only 1 Category can be requested per API Call.
        To get questions from any category, don't specify a category.
        A Maximum of 50 Questions can be retrieved per call.

        :param num_questions: the number of questions,
        must be between 1 and 50 (inclusive)

        :param category: the category of the question. None for any category

        :param diffculty: the diffculty of the question. None for any diffculty

        :param type_: the type of the question. None for any type

        :return: the api call response

        :rtype: dict

        :raises: ValueError when the num_questions parameter is less than 1
        or greater than 50
        """
        if num_questions < 1 or num_questions > 50:
            raise ValueError
        url = 'https://opentdb.com/api.php?amount={}&encode=base64'.format(
            num_questions)
        if category is not None:
            url += '&category={}'.format(category.value)
        if diffculty is not None:
            url += '&difficulty={}'.format(diffculty.value)
        if type_ is not None:
            url += '&type={}'.format(type_.value)
        if self.token is not None:
            url += '&token={}'.format(self.token)
        result = loads(get(url).content)
        if result['response_code'] in (3, 4):
            self.token = _get_token()
            return self.request(num_questions, category, diffculty, type_)
        else:
            return _decode_dict(result)


def _decode_dict(d):
    """
    Recursivly decode all strings in a dict
    :param d: the input dict
    :return: a dict with all its vals decoded
    """
    if isinstance(d, int):
        return d
    elif isinstance(d, str):
        return _decode(d)
    elif isinstance(d, list):
        return [_decode_dict(s) for s in d]
    elif isinstance(d, dict):
        return {k: _decode_dict(v) for k, v in d.items()}


def _decode(s: str):
    """
    Deconde a base64 string into utf8
    :param s: the base64 encoded string
    :return: the utf-8 decoded string
    """
    try:
        return b64decode(s).decode('utf-8')
    except binascii.Error:
        return s


def _get_token():
    """
    Get a session token
    :return: a session token
    """
    return loads(
        get(
            'https://opentdb.com/api_token.php?command=request'
        ).content
    )['token']
