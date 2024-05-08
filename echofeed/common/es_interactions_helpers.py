"""
A module that contains helper functions for interacting with Elasticsearch.
"""
import requests
from elasticsearch import Elasticsearch

from echofeed.common import config_info
from echofeed.common.config_info import ElasticsearchIndexes as EsIndexes

logger = config_info.get_logger()


def get_elasticsearch_client() -> Elasticsearch:
    """
    Generates an Elasticsearch client with
    information from the configuration module.
    """
    es_client = Elasticsearch(config_info.ELASTICSEARCH_URL)
    logger.info("Generated Elasticsearch client")
    return es_client


def create_entity(entity_type: str, entity_info: dict) -> dict:
    """
    Adds a new entity instance to the database.
    """
    entity_index = EsIndexes.INDEXES[entity_type]
    response = {
        "message": f"Successfully added {entity_type} into the database",
        "code": 200,
        "result": True,
        f"{entity_type}_id": None
    }
    try:
        es_client = get_elasticsearch_client()
        new_entity = es_client.index(
            index=entity_index,
            document=entity_info
        )
        new_entity_dict = dict(new_entity)
        response[f"{entity_type}_id"] = new_entity_dict["_id"]
        logger.info(f"Added {entity_type} in the database: {new_entity_dict}")

    except Exception as exception:
        exception_message = (
            f"Encountered an exception when trying to add"
            f" a new {entity_type} into the database: {exception}"
        )
        logger.error(exception_message)
        response.update({
            "message": exception_message,
            "code": 424,
            "result": False
        })

    return response


def update_entity(entity_type: str, entity_id: str, entity_info: dict) -> dict:
    """
    Modifies an entity instance in the database.
    """
    entity_index = EsIndexes.INDEXES[entity_type]
    response = {
        "message": f"Successfully updated {entity_type} in the database",
        "code": 200,
        "result": True
    }
    try:
        es_client = get_elasticsearch_client()
        updated_entity = es_client.update(
            index=entity_index,
            id=entity_id,
            body={"doc": entity_info}
        )
        updated_entity_dict = dict(updated_entity)
        logger.info(f"Updated {entity_type} in the database:"
                    f" {updated_entity_dict}")

    except Exception as exception:
        exception_message = (
            f"Encountered an exception when trying to update"
            f" {entity_type} in the database: {exception}"
        )
        logger.error(exception_message)
        response.update({
            "message": exception_message,
            "code": 424,
            "result": False
        })

    return response


def delete_entity(entity_type: str, entity_id: str) -> dict:
    """
    Removes an entity instance from the database.
    """
    entity_index = EsIndexes.INDEXES[entity_type]
    response = {
        "message": f"Successfully deleted {entity_type} from the database",
        "code": 200,
        "result": True
    }
    try:
        es_client = get_elasticsearch_client()
        es_client.delete(index=entity_index, id=entity_id)
        logger.info(f"Deleted {entity_type} from the database")

    except Exception as exception:
        exception_message = (
            f"Encountered an exception when trying to delete"
            f" {entity_type} from the database: {exception}"
        )
        logger.error(exception_message)
        response.update({
            "message": exception_message,
            "code": 424,
            "result": False
        })

    return response


def search_entity(entity_type: str, search_query: dict) -> dict:
    """
    Searches for entity instances in the database.
    """
    entity_index = EsIndexes.INDEXES[entity_type]
    response = {
        "message": f"Successfully retrieved {entity_type} from the database",
        "code": 200,
        "result": True,
        f"{entity_type}s": []
    }
    try:
        es_client = get_elasticsearch_client()
        search_results = es_client.search(
            index=entity_index,
            body=search_query)
        response[f"{entity_type}s"] = search_results["hits"]["hits"]
        logger.info(f"Retrieved {entity_type} from the database:"
                    f" {search_results}")

    except Exception as exception:
        exception_message = (
            f"Encountered an exception when trying to retrieve"
            f" {entity_type} from the database: {exception}"
        )
        logger.error(exception_message)
        response.update({
            "message": exception_message,
            "code": 424,
            "result": False
        })

    return response


def get_entity(entity_type: str, entity_id: str) -> dict:
    """
    Retrieves an entity instance from the database.
    """
    entity_index = EsIndexes.INDEXES[entity_type]
    response = {
        "message": f"Successfully retrieved {entity_type} from the database",
        "code": 200,
        "result": True,
        f"{entity_type}_info": None
    }
    try:
        es_client = get_elasticsearch_client()
        entity = es_client.get(index=entity_index, id=entity_id)
        response[f"{entity_type}_info"] = entity["_source"]
        logger.info(f"Retrieved {entity_type} from the database: "
                    f"{response[f'{entity_type}_info']}")

    except Exception as exception:
        exception_message = (
            f"Encountered an exception when trying to retrieve"
            f" {entity_type} from the database: {exception}"
        )
        logger.error(exception_message)
        response.update({
            "message": exception_message,
            "code": 424,
            "result": False
        })

    return response


def get_all_entities(entity_type: str) -> dict:
    """
    Gets all entities of the same type from elasticsearch index
    """
    response = {
        "message": f"Successfully retrieved {EsIndexes.INDEXES[entity_type]}"
                   f" from the database",
        "code": 200,
        "result": True,
        f"{EsIndexes.INDEXES[entity_type]}_info": None
    }

    try:
        response[f"{EsIndexes.INDEXES[entity_type]}_info"] = None
        entities_list = requests.get(
            url=f"{config_info.ELASTICSEARCH_URL}"
                f"/{EsIndexes.INDEXES[entity_type]}/_search?pretty"
        ).json()["hits"]["hits"]

        response[f"{EsIndexes.INDEXES[entity_type]}_info"] = []
        for entity in entities_list:
            entity_dict = entity["_source"]
            entity_dict[f"{entity_type}_id"] = entity["_id"]

            response[f"{EsIndexes.INDEXES[entity_type]}_info"].append(
                entity_dict
            )
        logger.info(f"Retrieved all {EsIndexes.INDEXES[entity_type]} from"
                    f" the database")

    except Exception as exception:
        exception_message = (
            f"Encountered exception when tried to retrieve"
            f" {EsIndexes.INDEXES[entity_type]} from the"
            f" database: {exception}"
        )
        response.update({
            "message": exception_message,
            "code": 424,
            "result": False
        })

    return response


def get_entities_by_user(user_id: str, entity_type: str) -> dict:
    """
    Retrieves all entity instances of the same type that belong to a user.
    """
    entity_index = EsIndexes.INDEXES[entity_type]
    response = {
        "message": f"Successfully retrieved {entity_type} from the database",
        "code": 200,
        "result": True,
        f"{entity_type}s": []
    }
    try:
        es_client = get_elasticsearch_client()
        search_results = es_client.search(
            index=entity_index,
            body={"query": {"match": {"user_id": user_id}}}
        )
        response[f"{entity_type}s"] = search_results["hits"]["hits"]
        logger.info(f"Retrieved {entity_type} from the database:"
                    f" {search_results}")

    except Exception as exception:
        exception_message = (
            f"Encountered an exception when trying to retrieve"
            f" {entity_type} from the database: {exception}"
        )
        logger.error(exception_message)
        response.update({
            "message": exception_message,
            "code": 424,
            "result": False
        })

    return response
