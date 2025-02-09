"""Main project file for api service."""

import fastapi
import uvicorn
from fastapi.responses import JSONResponse  # , RedirectResponse

from echofeed.common import config_info, api_request_classes as api_req_cls
from echofeed.api import api_endpoint_helpers as api_helpers
from echofeed.common.config_info import AcceptedOperations as acceptedOps
from echofeed.common.config_info import Entity
from echofeed.common.config_info import ElasticsearchIndexes as esIndexes

app = fastapi.FastAPI(
    title="EchoFeed API",
    description="API for EchoFeed project.",
    version=config_info.VERSION
)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    """Redirect to the API documentation."""
    return fastapi.responses.RedirectResponse(url="/docs")


@app.post(acceptedOps.ROUTES[Entity.ARTICLE][acceptedOps.CREATE],
          tags=[esIndexes.INDEXES[Entity.ARTICLE]])
async def create_article(request: api_req_cls.CreateArticleRequest) \
        -> JSONResponse:
    """Adds a new article instance to the database.

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
    response = api_helpers.create_article(request)
    return JSONResponse(response)


@app.put(acceptedOps.ROUTES[Entity.ARTICLE][acceptedOps.UPDATE],
         tags=[esIndexes.INDEXES[Entity.ARTICLE]])
async def update_article(request: api_req_cls.UpdateArticleRequest) \
        -> JSONResponse:
    """Updates an article instance in the database.

            Args:
                request (dict):
                    article_id(str): The id of the article.
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
    response = api_helpers.update_article(request)
    return JSONResponse(response)


@app.delete(acceptedOps.ROUTES[Entity.ARTICLE][acceptedOps.DELETE],
            tags=[esIndexes.INDEXES[Entity.ARTICLE]])
async def delete_article(article_id: str) -> JSONResponse:
    """Deletes an article instance from the database.

        Args:
            article_id(str): The id of the article.

        Returns:
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.

    """
    response = api_helpers.delete_article(article_id)
    return JSONResponse(response)


@app.get(acceptedOps.ROUTES[Entity.ARTICLE][acceptedOps.GET],
         tags=[esIndexes.INDEXES[Entity.ARTICLE]])
async def get_article(article_id: str) -> JSONResponse:
    """Retrieves an article instance from the database.

        Args:
            article_id(str): The id of the article.

        Returns:
            article_info(dict): The information of the article.
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.

    """
    response = api_helpers.get_article(article_id)
    return JSONResponse(response)


@app.get(acceptedOps.ROUTES[Entity.ARTICLE][acceptedOps.GET_ALL],
            tags=[esIndexes.INDEXES[Entity.ARTICLE]])
async def get_all_articles() -> JSONResponse:
    """Retrieves all article instances from the database.

        Returns:
            articles_info(dict): The information of all articles.
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.

    """
    response = api_helpers.get_all_articles()
    return JSONResponse(response)


@app.post(acceptedOps.ROUTES[Entity.USER][acceptedOps.CREATE],
          tags=[esIndexes.INDEXES[Entity.USER]])
async def create_user(request: api_req_cls.CreateUserRequest) -> JSONResponse:
    """Adds a new user instance to the database.

        Args:
            request (dict):
                user_info(dict):
                    first_name (str): The first name of the user.
                    last_name (str): The last name of the user.
                    birthday (string): The birthday of the user.
                    location (str): The location of the user.
                    interests(List[str]): The interests of the user.
                    viewed_articles(List[str]): The user's viewed articles.
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
    response = api_helpers.create_user(request)
    return JSONResponse(response)


@app.put(acceptedOps.ROUTES[Entity.USER][acceptedOps.UPDATE],
         tags=[esIndexes.INDEXES[Entity.USER]])
async def update_user(request: api_req_cls.UpdateUserRequest) -> JSONResponse:
    """Updates a user instance in the database.

        Args:
            request (dict):
                user_id(str): The id of the user.
                user_info(dict):
                    first_name (str): The first name of the user.
                    last_name (str): The last name of the user.
                    birthday (date): The birthday of the user.
                    location (str): The location of the user.
                    interests(List[str]): The interests of the user.
                    viewed_articles(List[str]): The user's viewed articles.
                    liked_articles(List[str]): The liked articles of the user.
                    is_admin(bool): The admin status of the user.

        Returns:
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.

    """
    response = api_helpers.update_user(request)
    return JSONResponse(response)


@app.delete(acceptedOps.ROUTES[Entity.USER][acceptedOps.DELETE],
            tags=[esIndexes.INDEXES[Entity.USER]])
async def delete_user(user_id: str) -> JSONResponse:
    """Deletes a user instance from the database.

        Args:
            user_id(str): The id of the user.

        Returns:
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.

    """
    response = api_helpers.delete_user(user_id)
    return JSONResponse(response)


@app.get(acceptedOps.ROUTES[Entity.USER][acceptedOps.GET],
         tags=[esIndexes.INDEXES[Entity.USER]])
async def get_user(user_id: str) -> JSONResponse:
    """Retrieves a user instance from the database.

        Args:
            user_id(str): The id of the user.

        Returns:
            user_info(dict): The information of the user.
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.

    """
    response = api_helpers.get_user(user_id)
    return JSONResponse(response)


@app.get(acceptedOps.ROUTES[Entity.USER][acceptedOps.GET_ALL],
         tags=[esIndexes.INDEXES[Entity.USER]])
async def get_all_users() -> JSONResponse:
    """Retrieves all user instances from the database.

        Returns:
            users_info(dict): The information of all users.
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.

    """
    response = api_helpers.get_all_users()
    return JSONResponse(response)


@app.get(acceptedOps.ROUTES[Entity.USER][acceptedOps.LOGIN],
         tags=[esIndexes.INDEXES[Entity.USER]])
async def login(username: str, password: str) -> JSONResponse:
    """Logs in a user.

        Returns:
            user_info(dict): The information of the user.
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.

    """
    response = api_helpers.login(username, password)
    return JSONResponse(response)


@app.post(acceptedOps.ROUTES[Entity.ARTICLE][acceptedOps.SEARCH], tags=["search"])
async def search_articles(request: api_req_cls.SearchArticlesRequest) -> JSONResponse:
    """Searches articles through OpenAI API and Google Search API.

        Args:
            request (dict):
                important_keywords(List[str]): The important keywords.
                relevant_keywords(List[str]): The relevant keywords.
                irrelevant_keywords(List[str]): The irrelevant keywords.
                language(str): The language of the articles.
                min_keywords(int): The minimum number of keywords.
                num_results(int): The number of results.
                date(str): The date of the articles.

        Returns:
            articles_info(dict): The information of the articles.
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.

    """
    response = api_helpers.handle_article_search(
        request.important_keywords, request.relevant_keywords,
        request.irrelevant_keywords, request.language, request.min_keywords,
        request.num_results, request.date
    )
    return JSONResponse(response)


@app.post(acceptedOps.ROUTES[Entity.ARTICLE][acceptedOps.RECOMMENDATION], tags=["recommendation"])
async def get_recommendation(request: api_req_cls.GetRecommendationsRequest) -> JSONResponse:
    """Gets recommendations for a user.

        Args:
            request (dict):
                keywords(List[str]): The keywords.
                language(str): The language of the articles.
                date(str): The date of the articles.
        Returns:
            articles_info(dict): The information of the articles.
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.
    """
    response = api_helpers.handle_recommandation_search(
        request.keywords, request.language, request.date
    )
    return JSONResponse(response)


@app.get(acceptedOps.ROUTES[Entity.ARTICLE][acceptedOps.KEYWORDS], tags=["keywords"])
async def generate_keywords(request: api_req_cls.GetKeywordsRequest) -> JSONResponse:
    """Generates keywords for a user input.

        Args:
            user_input(str): The user input.
            language(str): The language of the keywords.

        Returns:
            keywords(List[str]): The generated keywords.
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.
            :param request:

    """
    response = api_helpers.handle_keywords_generation(request.user_input, request.language)
    return JSONResponse(response)


@app.get(acceptedOps.ROUTES[Entity.ARTICLE][acceptedOps.CATEGORIES], tags=["categories"])
async def get_categories(request: api_req_cls.GetCategoriesRequest) -> JSONResponse:
    """Gets categories for a list of keywords.

        Args:
            keywords(List[str]): The keywords.

        Returns:
            categories(dict): The categories.
            message(str): a message that contains information about
                          the operation.
            code(int): the result code of the operation.
            result(bool): the result of the operation.
            :param request:

    """
    response = api_helpers.handle_keywords_categorization(request.keywords)
    return JSONResponse(response)


if __name__ == "__main__":
    uvicorn.run(
        app=config_info.API_APP,
        host=config_info.HOST,
        port=config_info.API_PORT,
        reload=True
    )
