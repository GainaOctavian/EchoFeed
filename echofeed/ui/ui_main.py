import datetime

from nicegui import ui, app
import requests
from echofeed.common import config_info, api_request_classes, api_classes
import ui_authentication as auth
import ui_auth_middleware
import ui_helpers

app.add_middleware(ui_auth_middleware.AuthMiddleware)


def with_header(page_func):
    def wrapper():
        ui_helpers.page_header()
        page_func()
    return wrapper


@ui.page('/')
@with_header
def home_page() -> None:
    auth.home_page()

@ui.page('/login')
def login_page() -> None:
    auth.login_page()


@ui.page('/search-news')
@with_header
def search_page() -> None:
    app.storage.user['search_clicked'] = False
    with ui.column().classes('items-center w-full mx-auto my-8'):
        with ui.column().classes('w-full max-w-screen-lg mx-auto items-center'):
            ui.markdown('Search for news').classes('text-2xl mb-4')
            ui.label('What subject do you want to see news on?').classes('text-lg')
            language = ''
            important_keywords = []
            relevant_keywords = []
            irrelevant_keywords = []
            unselected_keywords = []  # Keywords that are not selected
            keyword_buttons = {}

            def set_language(value):
                nonlocal language
                language = value
                ui.notify(f'{language} selected', color='positive')

            def on_generate_button_click():
                generate_button.set_text('Generating...')
                keywords = ui_helpers.generate_keywords(user_input.value, language)
                display_keywords(keywords)
                generate_button.set_text('Regenerate Keywords')

            def display_keywords(keywords):
                for button in keyword_buttons.values():
                    button.delete()
                keyword_buttons.clear()

                if not keywords:
                    ui.notify("No keywords generated")
                else:
                    for keyword in keywords:
                        keyword_button = ui.button(keyword, on_click=lambda e, kw=keyword: toggle_keyword(kw))
                        keyword_button.classes('w-1/2 mt-2')
                        keyword_buttons[keyword] = keyword_button

            def toggle_keyword(keyword):
                if keyword in important_keywords:
                    important_keywords.remove(keyword)
                    relevant_keywords.append(keyword)
                elif keyword in relevant_keywords:
                    relevant_keywords.remove(keyword)
                    irrelevant_keywords.append(keyword)
                elif keyword in irrelevant_keywords:
                    irrelevant_keywords.remove(keyword)
                    unselected_keywords.append(keyword)
                elif keyword in unselected_keywords:
                    unselected_keywords.remove(keyword)
                    important_keywords.append(keyword)
                else:
                    important_keywords.append(keyword)
                update_keyword_styles(keyword)

            def update_keyword_styles(keyword):
                button = keyword_buttons[keyword]
                if keyword in important_keywords:
                    button.classes('bg-positive')
                    button.classes(remove='bg-warning bg-negative')
                elif keyword in relevant_keywords:
                    button.classes('bg-warning')
                    button.classes(remove='bg-negative bg-positive')
                elif keyword in irrelevant_keywords:
                    button.classes('bg-negative')
                    button.classes(remove='bg-positive bg-warning')
                elif keyword in unselected_keywords:
                    button.classes(remove='bg-positive bg-warning bg-negative')
                    button.classes('bg-primary')

            with ui.dropdown_button('Select language', auto_close=True).classes('mt-4'):
                ui.tooltip('Select the language you would like to use for the search').classes('cursor-pointer')
                ui.item('English', on_click=lambda: set_language('English'))
                ui.item('Romanian', on_click=lambda: set_language('Romanian'))

            ui.label('Please insert anything that you would like to see news on, in any language').classes('text-md')
            user_input = ui.input('Search').classes('w-1/2')

            generate_button = ui.button('Generate Keywords', on_click=on_generate_button_click).classes('mt-4 q-pa-md')
            with generate_button:
                ui.icon('key').classes('mr-2')
                ui.tooltip('Generate keywords based on the input text').classes('cursor-pointer')

        min_keywords = ui.input('Minimum keywords')
        with min_keywords:
            ui.tooltip('Minimum number of keywords to be used for the search.').classes('cursor-pointer')
        ui.label('Please insert the date after which the articles should be published').classes('text-md')
        after_date = ui.input('YYYY-MM-DD')
        with after_date.add_slot('append'):
            ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
            with ui.menu().props('position-anchor="bottom right" anchor="top left"') as menu:
                ui.date().bind_value(after_date)
        article_numbers = ui.input('Number of articles')
        with article_numbers:
            ui.tooltip('Number of articles to be displayed. Choosing too'
                       ' many might result into a failed search.').classes('cursor-pointer')

        def on_search_button_click():
            request = api_request_classes.SearchArticlesRequest(
                important_keywords=important_keywords,
                relevant_keywords=relevant_keywords,
                irrelevant_keywords=irrelevant_keywords,
                language=language,
                min_keywords=min_keywords.value,
                num_results=article_numbers.value,
                date=after_date.value
            )
            response = requests.post(
                f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.SEARCH]}",
                json=request.dict()
            )
            articles = []
            if response.status_code == 200:
                articles = response.json().get('articles', {})
            app.storage.user['articles'] = articles
            app.storage.user['search_clicked'] = True
            if articles:
                ui.notify('Search results have been loaded', color='positive')
            else:
                ui.notify('No articles found', color='negative')
            with ui.button(on_click=lambda: ui.navigate.to(
                                   '/search-results')).classes(
                'mt-4 q-pa-md') as results_button:
                ui.icon('visibility').classes('mr-2')
                ui.label('View search results')

        ui.button('Begin search!', on_click=on_search_button_click).classes('mt-4 q-pa-md')


@ui.page('/search-results')
@with_header
def search_results_page():
    if not app.storage.user.get('search_clicked', False):
        return ui.navigate.to('/search-news')

    serialized_articles = app.storage.user.get('articles', [])
    articles = [api_classes.Article(**article) for article in serialized_articles]

    app.storage.user['search_clicked'] = False
    ui.button('Back to search', on_click=lambda: ui.navigate.to('/search-news')).classes('q-pa-md')

    def on_click_like(article):
        response = requests.get(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}", params={'user_id': app.storage.user.get("username", "")})
        if response.status_code == 200:
            user_info = response.json().get("user_info", {})
            liked_articles = user_info.get("liked_articles", [])
            if article.title not in liked_articles:
                new_article = api_classes.Article(
                    title=article.title,
                    content=article.content,
                    url=article.url,
                    date=article.date,
                    keywords=article.keywords
                )
                response = requests.get(
                    f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.GET]}",
                    params={'article_id': article.title})
                if response.json().get("article_info", {}) is None:
                    request = api_request_classes.CreateArticleRequest(
                        article_info=new_article)
                    response = requests.post(
                        f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.CREATE]}",
                        json=request.dict())
                if response.status_code == 200:
                    ui.notify('Article found or added in the database',
                              color='positive')
                else:
                    ui.notify('Failed to add or find article in the database',
                              color='negative')
            liked_articles.append(article.title)
            updated_user = api_classes.User(
                username=user_info.get("username", ""),
                last_name=user_info.get("last_name", ""),
                first_name=user_info.get("first_name", ""),
                birthday=user_info.get("birthday", ""),
                location=user_info.get("location", ""),
                interests=user_info.get("interests", []),
                viewed_articles=user_info.get("viewed_articles", []),
                liked_articles=liked_articles,
                is_admin=user_info.get("is_admin", False),
                password=user_info.get("password", "")
            )
            request = api_request_classes.UpdateUserRequest(
                user_id=user_info.get("username", ""),
                user_info=updated_user)
            response = requests.put(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.UPDATE]}", json=request.dict())
            if response.status_code == 200:
                ui.notify('Article liked', color='positive')
                app.storage.user.update({'liked_articles': liked_articles})
            else:
                ui.notify('Failed to like article', color='negative')
        else:
            ui.notify('Failed to fetch user data', color='negative')

    def on_click_read_more(article):
        response = requests.get(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}", params={'user_id': app.storage.user.get("username", "")})
        if response.status_code == 200:
            user_info = response.json().get("user_info", {})
            viewed_articles = user_info.get("viewed_articles", [])
            if article.title not in viewed_articles:
                ui_helpers.get_or_create_article(article)
                viewed_articles.append(article.title)
                updated_user = api_classes.User(
                    username=user_info.get("username", ""),
                    last_name=user_info.get("last_name", ""),
                    first_name=user_info.get("first_name", ""),
                    birthday=user_info.get("birthday", ""),
                    location=user_info.get("location", ""),
                    interests=user_info.get("interests", []),
                    viewed_articles=viewed_articles,
                    liked_articles=user_info.get("liked_articles", []),
                    is_admin=user_info.get("is_admin", False),
                    password=user_info.get("password", "")
                )
                request = api_request_classes.UpdateUserRequest(
                    user_id=user_info.get("username", ""),
                    user_info=updated_user)
                response = requests.put(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.UPDATE]}", json=request.dict())
                if response.status_code == 200:
                    ui.notify('Article viewed', color='positive')
                    app.storage.user.update({'viewed_articles': viewed_articles})
                else:
                    ui.notify('Failed to view article', color='negative')
        ui.navigate.to(article.url, new_tab=True)

    with ui.column().classes('items-center w-full mx-auto my-8'):
        ui.markdown('Search results').classes('text-2xl mb-4')
        for article in articles:
            with ui.card().classes('w-full mx-auto q-pa-md'):
                ui.label(article.title).classes('text-lg')
                ui.label(article.date).classes('text-sm')
                ui.label(article.content).classes('text-md')
                ui.icon('favorite').on('click', lambda e, a=article: on_click_like(a)).classes('cursor-pointer text-2xl')
                with ui.button(on_click=lambda e, a=article: on_click_read_more(a)).classes('mt-4 q-pa-md'):
                    ui.icon('open_in_new').classes('mr-2')
                    ui.label('Read more')


@ui.page('/liked-articles')
@with_header
def liked_articles_page():
    def on_click_read_more(article):
        response = requests.get(
            f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}",
            params={'user_id': app.storage.user.get("username", "")})
        if response.status_code == 200:
            user_info = response.json().get("user_info", {})
            viewed_articles = user_info.get("viewed_articles", [])
            if article.title not in viewed_articles:
                viewed_articles.append(article.title)
                updated_user = api_classes.User(
                    username=user_info.get("username", ""),
                    last_name=user_info.get("last_name", ""),
                    first_name=user_info.get("first_name", ""),
                    birthday=user_info.get("birthday", ""),
                    location=user_info.get("location", ""),
                    interests=user_info.get("interests", []),
                    viewed_articles=viewed_articles,
                    liked_articles=user_info.get("liked_articles", []),
                    is_admin=user_info.get("is_admin", False),
                    password=user_info.get("password", "")
                )
                request = api_request_classes.UpdateUserRequest(
                    user_id=user_info.get("username", ""),
                    user_info=updated_user)
                response = requests.put(
                    f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.UPDATE]}",
                    json=request.dict())
                if response.status_code == 200:
                    ui.notify('Article viewed', color='positive')
                    app.storage.user.update(
                        {'viewed_articles': viewed_articles})
                else:
                    ui.notify('Failed to view article', color='negative')
        ui.navigate.to(article.url, new_tab=True)

    def on_click_remove(article):
        response = requests.get(
            f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}",
            params={'user_id': app.storage.user.get("username", "")})
        if response.status_code == 200:
            user_info = response.json().get("user_info", {})
            liked_articles = user_info.get("liked_articles", [])
            if article in liked_articles:
                liked_articles.remove(article)
                updated_user = api_classes.User(
                    username=user_info.get("username", ""),
                    last_name=user_info.get("last_name", ""),
                    first_name=user_info.get("first_name", ""),
                    birthday=user_info.get("birthday", ""),
                    location=user_info.get("location", ""),
                    interests=user_info.get("interests", []),
                    viewed_articles=user_info.get("viewed_articles", []),
                    liked_articles=liked_articles,
                    is_admin=user_info.get("is_admin", False),
                    password=user_info.get("password", "")
                )
                request = api_request_classes.UpdateUserRequest(
                    user_id=user_info.get("username", ""),
                    user_info=updated_user)
                response = requests.put(
                    f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.UPDATE]}",
                    json=request.dict())
                if response.status_code == 200:
                    ui.notify('Article removed from liked list',
                              color='positive')
                    ui.navigate.reload()
                else:
                    ui.notify('Failed to update liked articles',
                              color='negative')
            else:
                ui.notify('Article not found in liked articles',
                          color='negative')
        else:
            ui.notify('Failed to fetch user data', color='negative')

    if not app.storage.user.get('authenticated', False):
        return ui.navigate.to('/login')

    with ui.column().classes(
            'items-center w-full mx-auto'):
        ui.markdown('Liked articles').classes('text-2xl mb-4')

        response = requests.get(
            f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}",
            params={'user_id': app.storage.user.get("username", "")})

        if response.status_code == 200:
            liked_articles = response.json().get("user_info", {}).get(
                "liked_articles", [])
            if not liked_articles:
                ui.notify('You have not liked any articles yet',
                          color='negative')
            else:
                for article_id in liked_articles:
                    response = requests.get(
                        f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.GET]}",
                        params={'article_id': article_id})
                    article_data = response.json().get("article_info", {})

                    if article_data:
                        article = api_classes.Article(**article_data)
                        with ui.card().classes(
                                'w-full max-w-screen-lg mx-auto q-pa-md'):
                            ui.label(article.title).classes('text-lg')
                            ui.label(article.date).classes('text-sm')
                            ui.label(article.content).classes('text-md')
                            with ui.row().classes('items-center'):
                                with ui.button('', on_click=lambda e,
                                                                       a=article: on_click_read_more(
                                    a)).classes('mt-4 q-pa-md'):
                                    ui.icon('open_in_new').classes('mr-2')
                                    ui.label('Read more')
                                with ui.dialog() as dialog, ui.card().classes('items-center'):
                                    ui.label('Are you sure you want to remove this article from your liked articles?')
                                    with ui.row().classes('justify-end'):
                                        ui.button('Yes', on_click=lambda e,
                                                                         a=article_id: on_click_remove(
                                            a)).classes('bg-negative')
                                        ui.button('No',
                                                  on_click=dialog.close).classes(
                                            'bg-positive')
                                with ui.button('',
                                          on_click=dialog.open).classes('mt-4 q-pa-md self-end bg-negative'):
                                    ui.icon('delete').classes('mr-2')
                                    ui.label('Remove')

        else:
            ui.notify('Failed to fetch liked articles from the user',
                      color='negative')


@ui.page('/viewed-articles')
@with_header
def viewed_articles_page():
    if not app.storage.user.get('authenticated', False):
        return ui.navigate.to('/login')

    def on_click_clear(user_info):
        updated_user = api_classes.User(
            username=user_info.get("username", ""),
            last_name=user_info.get("last_name", ""),
            first_name=user_info.get("first_name", ""),
            birthday=user_info.get("birthday", ""),
            location=user_info.get("location", ""),
            interests=user_info.get("interests", []),
            viewed_articles=[],
            liked_articles=user_info.get("liked_articles", []),
            is_admin=user_info.get("is_admin", False),
            password=user_info.get("password", "")
        )
        request = api_request_classes.UpdateUserRequest(
            user_id=user_info.get("username", ""),
            user_info=updated_user)
        response = requests.put(
            f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.UPDATE]}",
            json=request.dict())
        if response.status_code == 200:
            ui.notify('Viewed articles cleared', color='positive')
            ui.navigate.reload()
        else:
            ui.notify('Failed to clear viewed articles', color='negative')

    with ui.column().classes(
            'items-center w-full mx-auto'):
        ui.markdown('Viewed articles').classes('text-2xl mb-4')
        response = requests.get(
            f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}",
            params={'user_id': app.storage.user.get("username", "")})
        if response.status_code == 200:
            user_info = response.json().get("user_info", {})
            liked_articles = user_info.get("viewed_articles", [])
            with ui.dialog() as dialog, ui.card().classes('items-center'):
                ui.label('Are you sure you want to clear your viewed articles?')
                with ui.row().classes('justify-end'):
                    ui.button('Yes', on_click=lambda e,
                                                       u=user_info: on_click_clear(
                        u)).classes('bg-negative')
                    ui.button('No', on_click=dialog.close).classes('bg-positive')
            with ui.button('',
                      on_click=dialog.open).classes(
                'q-pa-md mt-4 bg-negative'):
                ui.icon('delete').classes('mr-2')
                ui.label('Clear history')

            if not liked_articles:
                ui.notify('Your history is empty',
                          color='negative')
            else:
                for article in liked_articles:
                    response = requests.get(
                        f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.GET]}",
                        params={'article_id': article})
                    if response.status_code == 200:
                        retrieved_article = response.json().get("article_info",
                                                                {})
                        if retrieved_article is not None:
                            with ui.card().classes(
                                    'w-full max-w-screen-lg mx-auto q-pa-md'):
                                ui.label(retrieved_article.get('title',
                                                               '')).classes(
                                    'text-lg')
                                ui.label(
                                    retrieved_article.get('date', '')).classes(
                                    'text-sm')
                                ui.label(retrieved_article.get('content',
                                                               '')).classes(
                                    'text-md')
                                url = retrieved_article.get('url', '')
                                with ui.button('', on_click=lambda e, u=url: ui.navigate.to(u)).classes('mt-4 q-pa-md'):
                                    ui.icon('open_in_new').classes('mr-2')
                                    ui.label('Read more')
        else:
            ui.notify('Failed to fetch liked articles from the user',
                      color='negative')


@ui.page('/recommendations')
@with_header
def recommendations_page():
    if not app.storage.user.get('authenticated', False):
        return ui.navigate.to('/login')
    with ui.column().classes('absolute-center items-center w-full max-w-screen-lg mx-auto'):
        ui.markdown('Recommended articles').classes('text-2xl mb-4')

        response = requests.get(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}", params={'user_id': app.storage.user.get("username", "")})
        data = response.json()
        user_info = data.get("user_info", {})
        user_articles = user_info.get("liked_articles", [])

        articles_keywords = []
        response = requests.get(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.GET_ALL]}")
        all_articles = response.json().get("articles_info", [])
        recommended_articles = []
        selected_category = ""
        language = ""

        def set_language(value):
            nonlocal language
            language = value
            ui.notify(f'{language} selected', color='positive')

        def on_category_selected(category):
            ui.notify(f'{category} selected', color='positive')
            nonlocal selected_category
            selected_category = category

        def on_click_like(article):
            response = requests.get(
                f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}",
                params={'user_id': app.storage.user.get("username", "")})
            if response.status_code == 200:
                user_info = response.json().get("user_info", {})
                liked_articles = user_info.get("liked_articles", [])
                if article.title not in liked_articles:
                    new_article = api_classes.Article(
                        title=article.title,
                        content=article.content,
                        url=article.url,
                        date=article.date,
                        keywords=article.keywords
                    )
                    response = requests.get(
                        f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.GET]}",
                        params={'article_id': article.title})
                    if response.json().get("article_info", {}) is None:
                        request = api_request_classes.CreateArticleRequest(
                            article_info=new_article)
                        response = requests.post(
                            f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.CREATE]}",
                            json=request.dict())
                    if response.status_code == 200:
                        ui.notify('Article found or added in the database',
                                  color='positive')
                    else:
                        ui.notify(
                            'Failed to add or find article in the database',
                            color='negative')
                liked_articles.append(article.title)
                updated_user = api_classes.User(
                    username=user_info.get("username", ""),
                    last_name=user_info.get("last_name", ""),
                    first_name=user_info.get("first_name", ""),
                    birthday=user_info.get("birthday", ""),
                    location=user_info.get("location", ""),
                    interests=user_info.get("interests", []),
                    viewed_articles=user_info.get("viewed_articles", []),
                    liked_articles=liked_articles,
                    is_admin=user_info.get("is_admin", False),
                    password=user_info.get("password", "")
                )
                request = api_request_classes.UpdateUserRequest(
                    user_id=user_info.get("username", ""),
                    user_info=updated_user)
                response = requests.put(
                    f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.UPDATE]}",
                    json=request.dict())
                if response.status_code == 200:
                    ui.notify('Article liked', color='positive')
                    app.storage.user.update({'liked_articles': liked_articles})
                else:
                    ui.notify('Failed to like article', color='negative')
            else:
                ui.notify('Failed to fetch user data', color='negative')

        def on_click_read_more(article):
            response = requests.get(
                f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}",
                params={'user_id': app.storage.user.get("username", "")})
            if response.status_code == 200:
                user_info = response.json().get("user_info", {})
                viewed_articles = user_info.get("viewed_articles", [])
                if article.title not in viewed_articles:
                    ui_helpers.get_or_create_article(article)
                    viewed_articles.append(article.title)
                    updated_user = api_classes.User(
                        username=user_info.get("username", ""),
                        last_name=user_info.get("last_name", ""),
                        first_name=user_info.get("first_name", ""),
                        birthday=user_info.get("birthday", ""),
                        location=user_info.get("location", ""),
                        interests=user_info.get("interests", []),
                        viewed_articles=viewed_articles,
                        liked_articles=user_info.get("liked_articles", []),
                        is_admin=user_info.get("is_admin", False),
                        password=user_info.get("password", "")
                    )
                    request = api_request_classes.UpdateUserRequest(
                        user_id=user_info.get("username", ""),
                        user_info=updated_user)
                    response = requests.put(
                        f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.UPDATE]}",
                        json=request.dict())
                    if response.status_code == 200:
                        ui.notify('Article viewed', color='positive')
                        app.storage.user.update(
                            {'viewed_articles': viewed_articles})
                    else:
                        ui.notify('Failed to view article', color='negative')
            ui.navigate.to(article.url, new_tab=True)

        def show_recommendations():
            request = api_request_classes.GetRecommendationsRequest(
                keywords=categories[selected_category],
                language=language,
                date=after_date.value)

            response = requests.post(
                f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.RECOMMENDATION]}",
                json=request.dict())
            if response.status_code == 200:
                recommended_articles_dict = response.json().get('articles', [])
                recommended_articles  = [api_classes.Article(**article) for article in recommended_articles_dict]
            with scroll_area:
                for article in recommended_articles:
                    with ui.card().classes('w-full mx-auto q-pa-md'):
                        ui.label(article.title).classes('text-lg')
                        ui.label(article.date).classes('text-sm')
                        ui.label(article.content).classes('text-md')
                        ui.icon('favorite').on('click',
                                               lambda e, a=article: on_click_like(
                                                   a)).classes('cursor-pointer')
                        ui.button('Read more',
                                  on_click=lambda e, a=article: on_click_read_more(
                                      a)).classes('mt-4 q-pa-md')
            ui.notify('Recommendations generated', color='positive')

        for article in all_articles:
            if article.get("title", "") in user_articles:
                articles_keywords.extend(article.get("keywords", []))
        articles_keywords = list(set(articles_keywords))
        request = api_request_classes.GetCategoriesRequest(
            keywords=articles_keywords)
        response = requests.get(
            f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.CATEGORIES]}",
            json=request.dict())
        categories = response.json().get('categories', {})

        with ui.row():
            with ui.dropdown_button('Select language',
                                    auto_close=True).classes(
                    'mt-4'):
                ui.item('English', on_click=lambda: set_language('English'))
                ui.item('Romanian', on_click=lambda: set_language('Romanian'))

            with ui.dropdown_button('Select category',
                                    auto_close=True).classes('mt-4'):
                for category in categories.keys():
                    ui.item(category, on_click=lambda e,
                                                      c=category: on_category_selected(
                        c))
            after_date = ui.input('YYYY-MM-DD')
            with after_date.add_slot('append'):
                ui.icon('edit_calendar').on('click',
                                            lambda: menu.open()).classes(
                    'cursor-pointer')
                with ui.menu().props(
                        'position-anchor="bottom right" anchor="top left"') as menu:
                    ui.date().bind_value(after_date)
        ui.button('Get recommendations', on_click=show_recommendations).classes('mt-4 q-pa-md')
        scroll_area = ui.scroll_area().classes('w-full max-w-screen-lg mx-auto')


@ui.page('/users')
@with_header
def users_page():
    if not app.storage.user.get('authenticated', False) or not app.storage.user.get('is_admin', False):
        return ui.navigate.to('/')

    def on_click_remove():
        user_id = user.get("username", "")
        response = requests.delete(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.DELETE]}", params={'user_id': user_id})
        if response.status_code == 200:
            ui.notify('User removed', color='positive')
            ui.navigate.reload()
        else:
            ui.notify('Failed to remove user', color='negative')

    def on_click_change_admin_status(user):
        updated_user = api_classes.User(
            username=user.get("username", ""),
            last_name=user.get("last_name", ""),
            first_name=user.get("first_name", ""),
            birthday=user.get("birthday", ""),
            location=user.get("location", ""),
            interests=user.get("interests", []),
            viewed_articles=user.get("viewed_articles", []),
            liked_articles=user.get("liked_articles", []),
            is_admin=not user.get("is_admin", False),
            password=user.get("password", "")
        )
        request = api_request_classes.UpdateUserRequest(
            user_id=user.get("username", ""),
            user_info=updated_user)
        response = requests.put(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.UPDATE]}", json=request.dict())
        if response.status_code == 200:
            ui.notify(f"Admin status changed for user {user.get('username', '')}", color='positive')

    with ui.column().classes('items-center w-1/3 mx-auto'):
        ui.markdown('Users').classes('text-3xl mb-4')
        response = requests.get(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET_ALL]}")
        if response.status_code == 200:
            users = response.json().get("users_info", [])
            if not users:
                ui.notify('There are no users in the database', color='negative')
            else:
                for user in users:
                    with ui.card().style('background-color: #d7e3f4').classes('w-full mx-auto q-pa-md items-center py-8'):
                        ui.label(f"User: {user.get('username', '')}").classes('text-lg')
                        ui.label(f"Location: {user.get('location', '')}").classes('text-md')
                        ui.label(f"Birthday: {user.get('birthday', '')}").classes('text-md')
                        ui.button('Make user admin' if not user.get("is_admin", False) else 'Remove admin status', on_click=lambda e, u=user: on_click_change_admin_status(u)).classes('')
                        ui.button('Remove user', on_click=on_click_remove).classes('')
        else:
            ui.notify('Failed to fetch users', color='negative')


@ui.page('/profile')
@with_header
def profile_page() -> None:
    with ui.column().classes('absolute-center items-center h-4/5 w-full'
                             ' max-w-screen-lg mx-auto'):
        ui.markdown(f'Welcome to your profile,'
                    f' **{app.storage.user.get("username", "")}**!').classes(
            'text-2xl mb-4')

        response = requests.get(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}", params={'user_id': app.storage.user.get("username", "")})

        def remove_account():
            response = requests.delete(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.DELETE]}", params={'user_id': app.storage.user.get("username", "")})
            if response.status_code == 200:
                app.storage.user.clear()
                ui.notify('Account removed', color='positive')
                ui.navigate.to('/login')
            else:
                ui.notify('Failed to remove account', color='negative')

        if response.status_code == 200:
            data = response.json().get("user_info", {})
            with ui.column().classes('items-center'):
                ui.markdown('You are an **admin**' if data.get("is_admin", False) else 'You are **not** an **admin**').classes('text-lg')
                with ui.column():
                    ui.label(f'Your last name').classes('text-lg')
                    updated_last_name = ui.input(data.get("last_name", "")).classes('text-lg')
                with ui.column():
                    ui.label(f'Your first name').classes('text-lg')
                    updated_first_name = ui.input(data.get("first_name", "")).classes('text-lg')
                with ui.column():
                    ui.label(f'Your location').classes('text-lg')
                    updated_location = ui.input(data.get("location", "")).classes('text-lg')
                with ui.column():
                    ui.label(f'Your birthdate').classes('text-lg')
                    updated_birthday = ui.input(data.get("birthday", "")).classes('text-lg')
                    with updated_birthday.add_slot('append'):
                        ui.icon('edit_calendar').on('click',
                                                    lambda: menu.open()).classes(
                            'cursor-pointer')
                        with ui.menu().props(
                                'position-anchor="bottom right" anchor="top left"') as menu:
                            ui.date().bind_value(updated_birthday)
        else:
            ui.notify('Failed to fetch user data', color='negative')

        def on_click_modify_account(user, updated_last_name, updated_first_name, updated_birthday, updated_location):
            try:
                updated_birthday = str(
                    datetime.datetime.strptime(updated_birthday.value,
                                               '%Y-%m-%d').date())
            except ValueError:
                ui.notify(
                    'Birth date is not in the correct format (YYYY-MM-DD)',
                    color='negative')
                return
            if (updated_location.value == ""):
                updated_location.value = user.get("location", "")
            if (updated_last_name.value == ""):
                updated_last_name.value = user.get("last_name", "")
            if (updated_first_name.value == ""):
                updated_first_name.value = user.get("first_name", "")
            if (updated_birthday == ""):
                updated_birthday.value = user.get("birthday", "")

            request = api_request_classes.UpdateUserRequest(
                user_id=user.get("username", ""),
                user_info=api_classes.User(
                    username=user.get("username", ""),
                    last_name=updated_last_name.value,
                    first_name=updated_first_name.value,
                    birthday=updated_birthday,
                    location=updated_location.value,
                    interests=user.get("interests", []),
                    viewed_articles=user.get("viewed_articles", []),
                    liked_articles=user.get("liked_articles", []),
                    is_admin=user.get("is_admin", False),
                    password=user.get("password", "")
                )
            )
            response = requests.put(f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.UPDATE]}", json=request.dict())
            if response.status_code == 200:
                ui.notify('Account updated', color='positive')
                ui.navigate.reload()

        def on_click_remove_account(user):
            response = requests.delete(
                f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.DELETE]}",
                params={'user_id': user.get("username", "")}
            )
            if response.status_code == 200:
                app.storage.user.clear()
                ui.notify('Account removed', color='positive')
                ui.navigate.to('/login')

        with ui.dialog() as dialog_remove, ui.card().classes('items-center'):
            ui.label('Are you sure you want to remove your account?')
            with ui.row().classes('justify-end'):
                ui.button('Yes', on_click=lambda e,
                                                 u=data: on_click_remove_account(
                    u)).classes('bg-negative')
                ui.button('No', on_click=dialog_remove.close).classes('bg-positive')

        with ui.dialog() as dialog_modify, ui.card().classes('items-center'):
            ui.label('Do you want to save your changes?')
            with ui.row().classes('justify-end'):
                ui.button('Yes', on_click=lambda e,
                                                 u=data: on_click_modify_account(
                    u, updated_last_name, updated_first_name, updated_birthday, updated_location)).classes('bg-positive')
                ui.button('No', on_click=dialog_modify.close).classes('bg-negative')

        with ui.row():
            ui.button('Modify profile', on_click=dialog_modify.open).classes('mt-10 q-pa-md')
            ui.button('Delete account', on_click=dialog_remove.open).classes(
                'mt-10 q-pa-md bg-negative')


@ui.page('/register')
def register_page():
    return auth.register_page()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title='EchoFeed',
        host=config_info.HOST,
        port=config_info.UI_PORT,
        storage_secret='EchoFeed secret key'
    )
