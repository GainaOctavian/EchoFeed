"""Unit tests for the API endpoint helpers."""
from echofeed.api import api_endpoint_helpers as api_helpers
from echofeed.api import api_classes as api_cls
from echofeed.api import api_request_classes as api_req_cls


def test_create_article():
    """Test create_article function."""
    request = api_req_cls.CreateArticleRequest(
        article_info=api_cls.Article(
            title="test title",
            content="test content",
            keywords=["test keyword 1", "test keyword 2"],
        )
    )
    response = api_helpers.create_article(request)
    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200
    assert response["article_id"] is not None

    api_helpers.delete_article(response["article_id"])


def test_create_user():
    """Test create_user function."""
    request = api_req_cls.CreateUserRequest(
        user_info=api_cls.User(
            first_name="test first name",
            last_name="test last name",
            birthday="2000-01-01",
            location="test location",
            interests=["test interest 1", "test interest 2"],
            viewed_articles=["test article 1", "test article 2"],
            liked_articles=["test article 3", "test article 4"],
            is_admin=False,
        )
    )
    response = api_helpers.create_user(request)
    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200
    assert response["user_id"] is not None

def test_update_article():
    """Test update_article function."""
    create_request = api_req_cls.CreateArticleRequest(
        article_info=api_cls.Article(
            title="test title",
            content="test content",
            keywords=["test keyword 1", "test keyword 2"],
        )
    )
    response = api_helpers.create_article(create_request)
    test_article_id = response["article_id"]

    test_article_info = api_cls.Article(
        title="updated title",
        content="updated content",
        keywords=["updated keyword 1", "updated keyword 2"],
    )

    update_request = api_req_cls.UpdateArticleRequest(
        article_id=test_article_id,
        article_info=test_article_info
    )
    response = api_helpers.update_article(update_request)
    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200

    updated_article = api_helpers.get_article(test_article_id)["article_info"]

    expected_article_info = update_request.article_info.model_dump()
    assert updated_article == expected_article_info

    api_helpers.delete_article(test_article_id)


def test_update_user():
    """Test update_user function."""
    create_request = api_req_cls.CreateUserRequest(
        user_info=api_cls.User(
            first_name="test first name",
            last_name="test last name",
            birthday="2000-01-01",
            location="test location",
            interests=["test interest 1", "test interest 2"],
            viewed_articles=["test article 1", "test article 2"],
            liked_articles=["test article 3", "test article 4"],
            is_admin=False,
        )
    )
    response = api_helpers.create_user(create_request)
    test_user_id = response["user_id"]

    test_user_info = api_cls.User(
        first_name="updated first name",
        last_name="updated last name",
        birthday="2000-01-01",
        location="updated location",
        interests=["updated interest 1", "updated interest 2"],
        viewed_articles=["updated article 1", "updated article 2"],
        liked_articles=["updated article 3", "updated article 4"],
        is_admin=True,
    )

    update_request = api_req_cls.UpdateUserRequest(
        user_id=test_user_id,
        user_info=test_user_info
    )
    response = api_helpers.update_user(update_request)
    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200

    updated_user = api_helpers.get_user(test_user_id)["user_info"]

    expected_user_info = update_request.user_info.model_dump()
    expected_user_info["birthday"] = str(expected_user_info["birthday"])
    assert updated_user == expected_user_info

    api_helpers.delete_user(test_user_id)


def test_get_article():
    """Test get_article function."""
    request = api_req_cls.CreateArticleRequest(
        article_info = api_cls.Article(
            title="test title",
            content="test content",
            keywords=["test keyword 1", "test keyword 2"],
        )
    )
    response = api_helpers.create_article(request)

    test_article_id = response["article_id"]
    response = api_helpers.get_article(test_article_id)

    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200

    expected_article_info = request.article_info.model_dump()
    assert response["article_info"] == expected_article_info

    api_helpers.delete_article(test_article_id)


def test_get_user():
    """Test get_user function."""
    request = api_req_cls.CreateUserRequest(
        user_info=api_cls.User(
            first_name="test first name",
            last_name="test last name",
            birthday="2000-01-01",
            location="test location",
            interests=["test interest 1", "test interest 2"],
            viewed_articles=["test article 1", "test article 2"],
            liked_articles=["test article 3", "test article 4"],
            is_admin=False,
        )
    )
    response = api_helpers.create_user(request)

    test_user_id = response["user_id"]
    response = api_helpers.get_user(test_user_id)

    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200

    expected_user_info = request.user_info.model_dump()
    expected_user_info["birthday"] = str(expected_user_info["birthday"])
    assert response["user_info"] == expected_user_info

    api_helpers.delete_user(test_user_id)


def test_delete_article():
    """Test delete_article function."""
    request = api_req_cls.CreateArticleRequest(
        article_info=api_cls.Article(
            title="test title",
            content="test content",
            keywords=["test keyword 1", "test keyword 2"],
        )
    )
    response = api_helpers.create_article(request)

    test_article_id = response["article_id"]
    response = api_helpers.delete_article(test_article_id)

    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200

    response = api_helpers.get_article(test_article_id)
    assert "Error" in response["message"]
    assert response["result"] is False
    assert response["code"] == 404


def test_delete_user():
    """Test delete_user function."""
    request = api_req_cls.CreateUserRequest(
        user_info=api_cls.User(
            first_name="test first name",
            last_name="test last name",
            birthday="2000-01-01",
            location="test location",
            interests=["test interest 1", "test interest 2"],
            viewed_articles=["test article 1", "test article 2"],
            liked_articles=["test article 3", "test article 4"],
            is_admin=False,
        )
    )
    response = api_helpers.create_user(request)

    test_user_id = response["user_id"]
    response = api_helpers.delete_user(test_user_id)

    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200

    response = api_helpers.get_user(test_user_id)
    assert "Error" in response["message"]
    assert response["result"] is False
    assert response["code"] == 404
