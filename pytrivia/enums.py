from enum import Enum

__all__ = ['Category', 'Diffculty', 'Type']


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
