from nicegui import ui, app
import requests
from echofeed.common import config_info, api_request_classes, api_classes

API_BASE_URL = f"http://{config_info.HOST}:{config_info.API_PORT}"


def page_header():
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between mb-12'):
        ui.button(on_click=lambda: drawer.toggle(), icon='menu').props('flat color=white')
        dark = ui.dark_mode()
        with ui.row().classes('justify-center items-center'):
            ui.icon('campaign', color='white').classes('text-4xl')
            ui.label('EchoFeed').classes('text-white text-2xl')
        ui.switch('Switch mode', on_change=lambda e: dark.toggle())

    drawer = ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4').classes('items-center')
    with drawer:
        ui.label('Menu').classes('text-lg text-center')
        with ui.button('', on_click=lambda: ui.navigate.to('/')).classes('w-full'):
            ui.icon('home').classes('mr-2')
            ui.label('Home')
        with ui.button('', on_click=lambda: ui.navigate.to('/search-news')).classes('w-full'):
            ui.icon('search').classes('mr-2')
            ui.label('Search News')
        with ui.button('', on_click=lambda: ui.navigate.to('/liked-articles')).classes('w-full'):
            ui.icon('thumb_up').classes('mr-2')
            ui.label('Liked Articles')
        with ui.button('', on_click=lambda: ui.navigate.to('/viewed-articles')).classes('w-full'):
            ui.icon('history').classes('mr-2')
            ui.label('Viewed Articles')
        with ui.button('', on_click=lambda: ui.navigate.to('/recommendations')).classes('w-full'):
            ui.icon('star').classes('mr-2')
            ui.label('Recommendations')
        if(app.storage.user.get('is_admin', False)):
            with ui.button('', on_click=lambda: ui.navigate.to('/users')).classes('w-full'):
                ui.icon('people').classes('mr-2')
                ui.label('Users')
        with ui.button('', on_click=lambda: ui.navigate.to('/profile')).classes('w-full'):
            ui.icon('account_circle').classes('mr-2')
            ui.label('Profile')
        with ui.button('', on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/login'))).classes('w-full'):
            ui.icon('logout').classes('mr-2')
            ui.label('Log out')


def get_or_create_article(article):
    new_article = api_classes.Article(
        title=article.title,
        content=article.content,
        url=article.url,
        date=article.date,
        keywords=article.keywords
    )
    response = requests.get(
        f"{API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.GET]}",
        params={'article_id': article.title})
    if response.json().get("article_info", {}) is None:
        request = api_request_classes.CreateArticleRequest(
            article_info=new_article)
        response = requests.post(
            f"{API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.CREATE]}",
            json=request.dict())
    if response.status_code == 200:
        ui.notify('Article found or added in the database',
                  color='positive')
    else:
        ui.notify('Failed to add or find article in the database',
                  color='negative')


def generate_keywords(user_input: str, language: str):
    request = api_request_classes.GetKeywordsRequest(
        user_input=user_input,
        language=language
    )
    response = requests.get(
        f"{API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.KEYWORDS]}",
        json=request.dict())
    keywords = response.json().get("keywords", [])
    return keywords
