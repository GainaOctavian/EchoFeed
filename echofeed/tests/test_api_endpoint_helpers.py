"""Unit tests for the API endpoint helpers."""
from datetime import datetime

import bcrypt

from echofeed.common import config_info, api_request_classes as api_req_cls, api_classes as api_cls
from echofeed.api import api_endpoint_helpers as api_helpers


def test_create_article():
    """Test create_article function."""
    request = api_req_cls.CreateArticleRequest(
        article_info=api_cls.Article(
            title="test title",
            content="test content",
            url="test url",
            date="2021-01-01",
            keywords=["test keyword 1", "test keyword 2"],
        )
    )
    response = api_helpers.create_article(request)
    api_helpers.delete_article(response["article_id"])

    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200
    assert response["article_id"] is not None


def test_create_user():
    """Test create_user function."""
    unique_username = "test_username_" + str(datetime.now().timestamp())
    user_info = api_cls.User(
        username=unique_username,
        first_name="test first name",
        last_name="test last name",
        birthday="2000-01-01",
        location="test location",
        interests=["test interest 1", "test interest 2"],
        viewed_articles=["test article 1", "test article 2"],
        liked_articles=["test article 3", "test article 4"],
        is_admin=False,
        password="test password",
    )
    request = api_req_cls.CreateUserRequest(user_info=user_info)
    response = api_helpers.create_user(request)

    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200
    assert response["user_id"] is not None

    # Cleanup
    api_helpers.delete_user(unique_username)


def test_update_article():
    """Test update_article function."""
    create_request = api_req_cls.CreateArticleRequest(
        article_info=api_cls.Article(
            title="test title",
            content="test content",
            url="test url",
            date=datetime.strptime("2021-01-01",
                                   "%Y-%m-%d").date(),
            keywords=["test keyword 1", "test keyword 2"],
        )
    )
    response = api_helpers.create_article(create_request)
    test_article_id = response["article_id"]

    test_article_info = api_cls.Article(
        title="updated title",
        content="updated content",
        url="updated url",
        date=datetime.strptime("2021-01-01",
                               "%Y-%m-%d").date(),
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

    # Adjust the comparison for the date field
    expected_article_info = update_request.article_info.model_dump()
    updated_article["date"] = datetime.strptime(updated_article["date"],
                                                "%Y-%m-%d").date()

    assert updated_article == expected_article_info

    api_helpers.delete_article(test_article_id)


def test_update_user():
    """Test update_user function."""
    unique_username = "test_username_" + str(datetime.now().timestamp())
    user_info = api_cls.User(
        username=unique_username,
        first_name="test first name",
        last_name="test last name",
        birthday="2000-01-01",
        location="test location",
        interests=["test interest 1", "test interest 2"],
        viewed_articles=["test article 1", "test article 2"],
        liked_articles=["test article 3", "test article 4"],
        is_admin=False,
        password="test password",
    )
    create_request = api_req_cls.CreateUserRequest(user_info=user_info)
    response = api_helpers.create_user(create_request)
    test_username = user_info.username

    updated_user_info = api_cls.User(
        username=test_username,
        first_name="updated first name",
        last_name="updated last name",
        birthday="2000-01-01",
        location="updated location",
        interests=["updated interest 1", "updated interest 2"],
        viewed_articles=["updated article 1", "updated article 2"],
        liked_articles=["updated article 3", "updated article 4"],
        is_admin=True,
        password="updated password",
    )

    update_request = api_req_cls.UpdateUserRequest(
        user_id=test_username,
        user_info=updated_user_info
    )
    response = api_helpers.update_user(update_request)
    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200

    updated_user = api_helpers.get_user(test_username)["user_info"]

    expected_user_info = update_request.user_info.model_dump()
    expected_user_info["birthday"] = str(expected_user_info["birthday"])
    assert updated_user == expected_user_info

    # Cleanup
    api_helpers.delete_user(test_username)


def test_get_article():
    """Test get_article function."""
    request = api_req_cls.CreateArticleRequest(
        article_info = api_cls.Article(
            title="test title",
            content="test content",
            url="test url",
            date=datetime.strptime("2021-01-01",
                                   "%Y-%m-%d").date(),
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

    # Adjust the comparison for the date field
    response_article_info = response["article_info"]
    response_article_info["date"] = datetime.strptime(
        response_article_info["date"], "%Y-%m-%d").date()

    assert response_article_info == expected_article_info


def test_get_user():
    """Test get_user function."""
    unique_username = "test_username_" + str(datetime.now().timestamp())
    user_info = api_cls.User(
        username=unique_username,
        first_name="test first name",
        last_name="test last name",
        birthday="2000-01-01",
        location="test location",
        interests=["test interest 1", "test interest 2"],
        viewed_articles=["test article 1", "test article 2"],
        liked_articles=["test article 3", "test article 4"],
        is_admin=False,
        password="test password",
    )
    request = api_req_cls.CreateUserRequest(user_info=user_info)
    response = api_helpers.create_user(request)
    test_username = user_info.username

    response = api_helpers.get_user(test_username)
    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200

    expected_user_info = response["user_info"]
    expected_user_info["birthday"] = str(expected_user_info["birthday"])
    assert response["user_info"] == expected_user_info

    api_helpers.delete_user(test_username)


def test_delete_article():
    """Test delete_article function."""
    request = api_req_cls.CreateArticleRequest(
        article_info=api_cls.Article(
            title="test title",
            content="test content",
            url="test url",
            date=datetime.strptime("2021-01-01",
                                   "%Y-%m-%d"),
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
    unique_username = "test_username_" + str(datetime.now().timestamp())
    user_info = api_cls.User(
        username=unique_username,
        first_name="test first name",
        last_name="test last name",
        birthday="2000-01-01",
        location="test location",
        interests=["test interest 1", "test interest 2"],
        viewed_articles=["test article 1", "test article 2"],
        liked_articles=["test article 3", "test article 4"],
        is_admin=False,
        password="test password",
    )
    request = api_req_cls.CreateUserRequest(user_info=user_info)
    response = api_helpers.create_user(request)
    test_user_id = response["user_id"]

    response = api_helpers.delete_user(test_user_id)

    assert "Success" in response["message"]
    assert response["result"] is True
    assert response["code"] == 200

    # Verifică dacă utilizatorul a fost șters
    response = api_helpers.get_user(test_user_id)
    assert response["message"] == f"User with id {test_user_id} not found"
    assert response["result"] is False
    assert response["code"] == 404


def test_login():
    """Test login function."""
    unique_username = "test_username_" + str(datetime.now().timestamp())
    user_info = api_cls.User(
        username=unique_username,
        first_name="test first name",
        last_name="test last name",
        birthday="2000-01-01",
        location="test location",
        interests=["test interest 1", "test interest 2"],
        viewed_articles=["test article 1", "test article 2"],
        liked_articles=["test article 3", "test article 4"],
        is_admin=False,
        password="1234",
    )
    request = api_req_cls.CreateUserRequest(user_info=user_info)
    api_helpers.create_user(request)

    response = api_helpers.login(username=unique_username, password="1234")
    assert response["result"] is True
    assert response["code"] == 200

    # Clean up
    api_helpers.delete_user(unique_username)


def test_hash_password():
    password = "test_password"
    hash1 = config_info.hash_password(password)
    hash2 = config_info.hash_password(password)

    # Verificăm că hash-urile sunt diferite
    assert hash1 != hash2, "Hash-urile generate pentru aceeași parolă nu ar trebui să fie identice"

    # Verificăm că ambele hash-uri sunt valide pentru parola originală
    assert bcrypt.checkpw(password.encode('utf-8'), hash1.encode(
        'utf-8')), "Primul hash nu este valid pentru parola originală"
    assert bcrypt.checkpw(password.encode('utf-8'), hash2.encode(
        'utf-8')), "Al doilea hash nu este valid pentru parola originală"
