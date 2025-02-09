"""File containing helper functions for the endpoints of the API service."""
from typing import List

from echofeed.common import config_info, api_request_classes as api_req_cls
from echofeed.common.config_info import Entity
from echofeed.common.config_info import ElasticsearchIndexes as esIndexes
from echofeed.common import es_interactions_helpers as es_helpers
from echofeed.api import api_google_search as api_search, api_gpt_interactions as api_gpt
from echofeed.common import api_classes as api_cls

logger = config_info.get_logger()


def create_article(request: api_req_cls.CreateArticleRequest) -> dict:
    """
    Adds a new article instance to the database.

    Args:
        request (dict):
            article_info(dict):
                title (str): The title of the article.
                content (str): The content of the article.
                url (str): The url of the article.
                date(str): The date of the article.
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
                username (str): The username of the user.
                last_name (str): The last name of the user.
                first_name (str): The first name of the user.
                birthday(str): The birthday of the user.
                location(str): The location of the user.
                interests(List[str]): The interests of the user.
                viewed_articles(List[str]): The viewed articles of the user.
                liked_articles(List[str]): The liked articles of the user.
                is_admin(bool): The admin status of the user.
                password(str): The password of the user.

    Returns:
        message(str): a message that contains information about
                      the operation.
        code(int): the result code of the operation.
        result(bool): the result of the operation.
        user_id(str): the id of the user, if the operation was
                      successful.
    """
    request.user_info.password = config_info.hash_password(request.user_info.password)

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
                url (str): The url of the article.
                date(str): The date of the article.
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
                username (str): The username of the user.
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
    if not response or not response.get('user_info'):
        return {
            "message": f"User with id {user_id} not found",
            "code": 404,
            "result": False,
            "user_info": None
        }

    logger.info(f"Retrieved user: {response}")
    logger.info(
        f"Hashed password: {response.get('user_info', {}).get('password', 'N/A')}")
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


def login(username: str, password: str) -> dict:
    try:
        print(f"Received password before hashing: {password}")  # for logging
        response = get_user(username)
        user = response.get('user_info', None)

        if user:
            stored_password = user['password']
            print(f"Stored password: {stored_password}")  # for logging
            if config_info.check_password(password, stored_password):
                return {
                    "user_info": user,
                    "message": "Login successful",
                    "code": 200,
                    "result": True
                }
            else:
                return {
                    "message": "Invalid password",
                    "code": 401,
                    "result": False
                }
        else:
            return {
                "message": "User doesn't exist(invalid username)",
                "code": 401,
                "result": False
            }
    except Exception as e:
        return {
            "message": f"Error during login: {e}",
            "code": 500,
            "result": False
        }


def handle_article_search(
        important_keywords: List[str], relevant_keywords: List[str],
        irrelevant_keywords: List[str], langauge: str, min_keywords: int,
        num_articles: int, date: str):
    """
    Handles the search for articles based on the given keywords.
    """
    query = api_gpt.extract_queries(important_keywords, relevant_keywords, irrelevant_keywords, langauge, min_keywords)

    keywords = important_keywords + relevant_keywords
    query = f"{query} after:{date}"

    articles = api_search.create_articles_from_search(query, keywords, num_articles)
    articles_dict = [article.dict() for article in articles]
    response = {
        "message": "Successfully created articles from search",
        "code": 200,
        "result": True,
        "articles": articles_dict
    }
    return response


def handle_recommandation_search(keywords: List[str], language: str, date:str):
    """
    Handles the recommandation of articles based on the given keywords.
    """
    query = api_gpt.extract_recommandation_queries(keywords, language)
    query = f"{query} after:{date}"
    articles = api_search.create_articles_from_search(query, keywords)
    articles_dict = [article.dict() for article in articles]
    response = {
        "message": "Successfully created articles from search",
        "code": 200,
        "result": True,
        "articles": articles_dict
    }
    return response


def handle_keywords_generation(user_input: str, language: str):
    """
    Handles the generation of keywords based on the user input.
    """
    keywords = api_gpt.generate_keywords(user_input, language)
    response = {
        "message": "Successfully generated keywords",
        "code": 200,
        "result": True,
        "keywords": keywords
    }
    return response


def handle_keywords_categorization(keywords: list):
    """
    Handles the categorization of keywords.
    """
    categories = api_gpt.categorize_keywords(keywords)
    response = {
        "message": "Successfully categorized keywords",
        "code": 200,
        "result": True,
        "categories": categories
    }
    return response

