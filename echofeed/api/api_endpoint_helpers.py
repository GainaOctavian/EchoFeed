"""File containing helper functions for the endpoints of the API service."""
from typing import List

from echofeed.common import config_info
from echofeed.common.config_info import Entity
from echofeed.common.config_info import ElasticsearchIndexes as esIndexes
from echofeed.common import es_interactions_helpers as es_helpers
from echofeed.api import api_request_classes as api_req_cls

logger = config_info.get_logger()


def create_article(request: api_req_cls.CreateArticleRequest) -> dict:
    """
    Adds a new article instance to the database.

    Args:
        request (dict):
            article_info(dict):
                title (str): The title of the article.
                content (str): The content of the article.
                keywords(List[str]): The keywords of the article.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
        article_id(str): the id of the article, if the operation was
                         successful.

    """
    response = es_helpers.create_entity(
        entity_type=Entity.ARTICLE,
        entity_info=request.article_info.model_dump()
    )
    logger.info(f"Created article: {response}")
    return response


def create_user(request: api_req_cls.CreateUserRequest) -> dict:
    """
    Adds a new user instance to the database.
    Args:
        request (dict):
            user_info(dict):
                last_name (str): The last name of the user.
                first_name (str): The first name of the user.
                birthday(str): The birthday of the user.
                location(str): The location of the user.
                interests(List[str]): The interests of the user.
                viewed_articles(List[str]): The viewed articles of the user.
                liked_articles(List[str]): The liked articles of the user.
                is_admin(bool): The admin status of the user.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
        user_id(str): the id of the user, if the operation was
                      successful.(???)
    """
    response = es_helpers.create_entity(
        entity_type=Entity.USER,
        entity_info=request.user_info.model_dump()
    )
    logger.info(f"Created user: {response}")
    return response


def update_article(request: api_req_cls.UpdateArticleRequest) -> dict:
    """
    Modifies an article instance in the database.

    Args:
        request (dict):
            article_info(dict):
                title (str): The title of the article.
                content (str): The content of the article.
                keywords(List[str]): The keywords of the article.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
    """
    response = es_helpers.update_entity(
        entity_type=Entity.ARTICLE,
        entity_id=request.article_id,
        entity_info=request.article_info.model_dump()
    )
    logger.info(f"Updated article: {response}")
    return response


def update_user(request: api_req_cls.UpdateUserRequest) -> dict:
    """
    Modifies a user instance in the database.

    Args:
        request (dict):
            user_info(dict):
                last_name (str): The last name of the user.
                first_name (str): The first name of the user.
                birthday(str): The birthday of the user.
                location(str): The location of the user.
                interests(List[str]): The interests of the user.
                viewed_articles(List[str]): The viewed articles of the user.
                liked_articles(List[str]): The liked articles of the user.
                is_admin(bool): The admin status of the user.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
    """
    response = es_helpers.update_entity(
        entity_type=Entity.USER,
        entity_id=request.user_id,
        entity_info=request.user_info.model_dump()
    )
    logger.info(f"Updated user: {response}")
    return response


def delete_user(user_id: str) -> dict:
    """
    Removes a user instance from the database.

    Args:
        user_id (str): The id of the user to be removed.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
    """
    response = es_helpers.delete_entity(
        entity_type=Entity.USER,
        entity_id=user_id
    )
    logger.info(f"Deleted user: {response}")
    return response


def delete_article(article_id: str) -> dict:
    """
    Removes an article instance from the database.

    Args:
        article_id (str): The id of the article to be removed.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
    """
    response = es_helpers.delete_entity(
        entity_type=Entity.ARTICLE,
        entity_id=article_id
    )
    logger.info(f"Deleted article: {response}")
    return response


def get_article(article_id: str) -> dict:
    """
    Retrieves an article instance from the database based on its id.

    Args:
        article_id (str): The id of the article to be retrieved.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
        article_info(dict): the information of the article, if the operation
                            was successful.
    """
    response = es_helpers.get_entity(
        entity_type=Entity.ARTICLE,
        entity_id=article_id
    )
    logger.info(f"Retrieved article: {response}")
    return response


def get_user(user_id: str) -> dict:
    """
    Retrieves a user instance from the database based on its id.

    Args:
        user_id (str): The id of the user to be retrieved.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
        user_info(dict): the information of the user, if the operation
                         was successful.
    """
    response = es_helpers.get_entity(
        entity_type=Entity.USER,
        entity_id=user_id
    )
    logger.info(f"Retrieved user: {response}")
    return response


GET_ENTITY_BY_TYPE = {
    Entity.ARTICLE: get_article,
    Entity.USER: get_user
}


def get_all_entities_from_list(entity_type: str, entity_ids: List[str])\
        -> dict:
    """
    Retrieves all Entity of a certain type from the database
    based on their ids.

    Args:
        entity_type (str): The type of the Entity to be retrieved.
        entity_ids (List[str]): The ids of the Entity to be retrieved.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
        Entity_info(dict): the information of the Entity, if the operation
                             was successful.
    """
    response = {
        "message": f"Successfully retrieved information about"
                   f" requested {esIndexes.INDEXES[entity_type]}",
        "code": 200,
        "result": True,
        f"{esIndexes.INDEXES[entity_type]}_info": {}
    }
    for entity_id in entity_ids:
        response[f"{esIndexes.INDEXES[entity_type]}_info"][entity_id] = (
            GET_ENTITY_BY_TYPE[entity_type](entity_id)[f"{entity_type}_info"]
        )
    logger.info(f"Returned response: {response}")
    return response


def get_all_users_from_list(request: api_req_cls.GetAllFromList) -> dict:
    """
    Retrieves all users from the database based on their ids.

    Args:
        request (dict):
            ids_list (List[str]): The ids of the users to be retrieved.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
        users_info(dict): the information of the users, if the operation
                          was successful.
    """
    user_ids_list = request.ids_list
    response = get_all_entities_from_list(
        entity_type=Entity.USER,
        entity_ids=user_ids_list
    )
    logger.info(f"Retrieved users: {response}")
    return response


def get_all_articles_from_list(request: api_req_cls.GetAllFromList) -> dict:
    """
    Retrieves all articles from the database based on their ids.

    Args:
        request (dict):
            ids_list (List[str]): The ids of the articles to be retrieved.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
        articles_info(dict): the information of the articles, if the operation
                             was successful.
    """
    article_ids_list = request.ids_list
    response = get_all_entities_from_list(
        entity_type=Entity.ARTICLE,
        entity_ids=article_ids_list
    )
    logger.info(f"Retrieved articles: {response}")
    return response


def get_all_users() -> dict:
    """
    Retrieves all users from the database.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
        users_info(dict): the information of the users, if the operation
                          was successful.
    """
    response = es_helpers.get_all_entities(entity_type=Entity.USER)
    logger.info(f"Retrieved users: {response}")
    return response


def get_all_articles() -> dict:
    """
    Retrieves all articles from the database.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
        articles_info(dict): the information of the articles, if the operation
                             was successful.
    """
    response = es_helpers.get_all_entities(entity_type=Entity.ARTICLE)
    logger.info(f"Retrieved articles: {response}")
    return response
