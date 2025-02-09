"""Confirguration information for the echofeed application."""
import hashlib
import logging
import sys

import bcrypt

VERSION = "v1"
HOST = "127.0.0.1"
API_PORT = 8080
API_APP = "api_main:app"
API_URL = f"http://127.0.0.1:{API_PORT}"

UI_PORT = 8081

OPENAI_API_KEY = 'sk-proj-sRJ1HoG2ixQllawPohkPT3BlbkFJYR1TEmY1vmRaQsk6SDZQ'
GOOGLE_API_KEY = 'AIzaSyBHiYY-Dvpdbr1Yc18-8UiozxgP8fSroO8'
GOOGLE_ENGINE_ID = '11530c2a1693b4f75'
GOOGLE_SEARCH_URL = 'https://www.googleapis.com/customsearch/v1'

ELASTICSEARCH_URL = "http://127.0.0.1:9200"
# ELASTICSEARCH_URL = "http://localhost:9200"

LOGGING_FORMAT = (
    "[%(asctime)s] [PID: %(process)d] [%(filename)s] "
    "[%(funcName)s: %(lineno)s] [%(levelname)s] %(message)s"
)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_logger():
    """
    Generates logger instance, logging messages in a specified format
    """
    logger = logging.getLogger("echofeed")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(LOGGING_FORMAT)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(handler)

    return logger


class Entity:
    """
    Class used to define constants for accepted Entity
    """
    ARTICLE = "article"
    USER = "user"


class ElasticsearchIndexes:
    """
    Class used to define constants for elasticsearch indexes
    """
    INDEXES = {
        Entity.ARTICLE: "articles",
        Entity.USER: "users"
    }


class AcceptedOperations:
    """
    Class used to define constants for accepted operations
    """
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    GET = "get"
    LOGIN = "login"
    GET_ALL = "get_all"
    GET_BY_USER = "get_by_user"
    SEARCH = "search"
    RECOMMENDATION = "recommendation"
    KEYWORDS = "keywords"
    CATEGORIES = "categories"

    ROUTES = {
        Entity.ARTICLE: {
            CREATE: f"/api/{VERSION}/articles",
            UPDATE: f"/api/{VERSION}/articles/",
            DELETE: f"/api/{VERSION}/articles/",
            GET: f"/api/{VERSION}/articles/",
            GET_ALL: f"/api/{VERSION}/articles/all/",
            GET_BY_USER: f"/api/{VERSION}/articles/users/",
            SEARCH: f"/api/{VERSION}/articles/search",
            RECOMMENDATION: f"/api/{VERSION}/articles/recommendation",
            KEYWORDS: f"/api/{VERSION}/articles/keywords",
            CATEGORIES: f"/api/{VERSION}/articles/categories"

        },
        Entity.USER: {
            CREATE: f"/api/{VERSION}/users",
            UPDATE: f"/api/{VERSION}/users/",
            DELETE: f"/api/{VERSION}/users/",
            GET: f"/api/{VERSION}/users/",
            LOGIN: f"/api/{VERSION}/users/login",
            GET_ALL: f"/api/{VERSION}/users/all/",
        }
    }
