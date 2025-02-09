"""Module containing request classes definitions for echofeed api service"""
from typing import List
from pydantic import BaseModel

from echofeed.common import api_classes as api_cls


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


class SearchArticlesRequest(BaseModel):
    """
    Request class for searching articles through
    openai api and google search api
    """
    important_keywords: list
    relevant_keywords: list
    irrelevant_keywords: list
    language: str
    min_keywords: int
    num_results: int
    date: str


class SearchArticlesResponse(BaseModel):
    """
    Response class for searching articles through
    openai api and google search api
    """
    articles: List[api_cls.Article]


class GetRecommendationsRequest(BaseModel):
    """
    Request class for getting recommendations
    """
    keywords: list
    language: str
    date: str


class GetRecommendationsResponse(BaseModel):
    """
    Response class for getting recommendations
    """
    articles: List[api_cls.Article]


class GetKeywordsRequest(BaseModel):
    """
    Request class for getting keywords
    """
    user_input: str
    language: str


class GetKeywordsResponse(BaseModel):
    """
    Response class for getting keywords
    """
    keywords: List[str]


class GetCategoriesRequest(BaseModel):
    """
    Request class for getting keyword categories
    """
    keywords: List[str]


class GetCategoriesResponse(BaseModel):
    """
    Response class for getting keyword categories
    """
    categories: dict

