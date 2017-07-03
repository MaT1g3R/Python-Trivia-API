# Python Trivia API
## Install
```
pip install Python-Trivia-API
```

## Example usage
```Python
from pytrivia import Category, Diffculty, Type, Trivia
my_api = Trivia(True)
response = my_api.request(2, Category.Books, Diffculty.Hard, Type.True_False)
print(response)
```

## Full method signature
```Python
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
```
