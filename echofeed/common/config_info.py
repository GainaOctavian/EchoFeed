"""Confirguration information for the echofeed application."""
import logging
import sys


VERSION = "v1"
HOST = "127.0.0.1"
API_PORT = 8080
API_APP = "api_main:app"

ELASTICSEARCH_URL = "http://127.0.0.1:9200"
# ELASTICSEARCH_URL = "http://localhost:9200"

LOGGING_FORMAT = (
    "[%(asctime)s] [PID: %(process)d] [%(filename)s] "
    "[%(funcName)s: %(lineno)s] [%(levelname)s] %(message)s"
)


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
    GET_ALL = "get_all"
    GET_BY_USER = "get_by_user"

    ROUTES = {
        Entity.ARTICLE: {
            CREATE: f"/api/{VERSION}/articles",
            UPDATE: f"/api/{VERSION}/articles/",
            DELETE: f"/api/{VERSION}/articles/",
            GET: f"/api/{VERSION}/articles/",
            GET_ALL: f"/api/{VERSION}/articles/all/",
            GET_BY_USER: f"/api/{VERSION}/articles/users/"

        },
        Entity.USER: {
            CREATE: f"/api/{VERSION}/users",
            UPDATE: f"/api/{VERSION}/users/",
            DELETE: f"/api/{VERSION}/users/",
            GET: f"/api/{VERSION}/users/",
            GET_ALL: f"/api/{VERSION}/users/all/",
        }
    }
