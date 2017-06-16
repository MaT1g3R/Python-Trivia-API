"""
A simple python api wrapper for https://opentdb.com/
"""

from aiohttp import ClientSession
from requests import get

from pytrivia.__helpers import decode_dict, get_token, make_request
from pytrivia.enums import *


class Trivia:
    def __init__(self, with_token: bool):
        """
        Initialize an instance of the Trivia class
        :param with_token: If True then the instance will uses a session token
        """
        self.token = get_token() if with_token else None

    def request(self, num_questions: int, category: Category = None,
                diffculty: Diffculty = None, type_: Type = None) -> dict:
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
        result = get(
            self.__url(num_questions, category, diffculty, type_)).json()
        if result['response_code'] in (3, 4):
            self.token = get_token()
            return self.request(num_questions, category, diffculty, type_)
        else:
            return decode_dict(result)

    async def request_async(self, session: ClientSession, close_session: bool,
                            num_questions: int, category: Category = None,
                            diffculty: Diffculty = None,
                            type_: Type = None) -> dict:
        """
        Send an api request to https://opentdb.com/
        Limitations:
        Only 1 Category can be requested per API Call.
        To get questions from any category, don't specify a category.
        A Maximum of 50 Questions can be retrieved per call.

        :param session: an Aiohttp client session.

        :param close_session: True to close the session after the request.

        :param num_questions: the number of questions,
        must be between 1 and 50 (inclusive)

        :param category: the category of the question. None for any category

        :param diffculty: the diffculty of the question. None for any diffculty

        :param type_: the type of the question. None for any type

        :return: the api call response

        :rtype: dict

        :raises: ValueError when the num_questions parameter is less than 1
        or greater than 50

        :raises ClientResponseError if the HTTP response code isn't 200
        """
        try:
            return await self.__request(
                session, num_questions, category, diffculty, type_)
        finally:
            if close_session:
                session.close()

    async def __request(self, session: ClientSession, num_questions: int,
                        category: Category = None, diffculty: Diffculty = None,
                        type_: Type = None) -> dict:
        """
        Helper method for the async request.
        """
        resp = await make_request(
            session, self.__url(num_questions, category, diffculty, type_))
        result = await resp.json()
        if result['response_code'] in (3, 4):
            self.token = get_token()
            return await self.__request(
                session, num_questions, category, diffculty, type_)
        else:
            return decode_dict(result)

    def __url(self, num_questions, category, diffculty, type_):
        """
        Helper method to generate request url.
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
        return url
