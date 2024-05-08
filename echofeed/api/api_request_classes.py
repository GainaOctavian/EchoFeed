"""Module containing request classes definitions for echofeed api service"""
from typing import List
from pydantic import BaseModel

from echofeed.api import api_classes as api_cls


class CreateArticleRequest(BaseModel):
    """
    Request class for create article operations
    """
    article_info: api_cls.Article


class CreateUserRequest(BaseModel):
    """
    Request class for create user operations
    """
    user_info: api_cls.User


class UpdateArticleRequest(BaseModel):
    """
    Request class for update article operations
    """
    article_id: str
    article_info: api_cls.Article


class UpdateUserRequest(BaseModel):
    """
    Request class for update user operations
    """
    user_id: str
    user_info: api_cls.User


class GetAllFromList(BaseModel):
    """
    Request class for get all from list operations
    """
    ids_list: List[str]
