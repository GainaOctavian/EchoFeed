"""
Module containing classes used for the API service
"""
from datetime import date
from typing import List
from pydantic import BaseModel


class Article(BaseModel):
    """
    Class that defines article object structure
    """
    title: str
    content: str
    keywords: List[str] = []  # optional?


class User(BaseModel):
    """
    Class that defines user object structure
    """
    last_name: str
    first_name: str
    birthday: date
    location: str
    interests: List[str] = []
    viewed_articles: List[str] = []  # the list contains either the article
    # id or the article title
    liked_articles: List[str] = []  # the list contains either the article
    # id or the article title
    is_admin: bool = False
