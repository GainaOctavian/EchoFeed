"""
Module containing classes used for the API service
"""
from typing import List, Optional
from pydantic import BaseModel


class Article(BaseModel):
    """
    Class that defines article object structure
    """
    title: str
    content: str
    url: str
    date: str
    keywords: Optional[List[str]]


class User(BaseModel):
    """
    Class that defines user object structure
    """
    username: str
    last_name: str
    first_name: str
    birthday: str
    location: str
    interests: List[str] = []
    viewed_articles: List[str] = []
    liked_articles: List[str] = []
    is_admin: bool = False
    password: str
