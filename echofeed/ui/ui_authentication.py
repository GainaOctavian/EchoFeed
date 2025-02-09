import datetime
import time

import requests
from fastapi.responses import RedirectResponse

from nicegui import app, ui

import echofeed.ui.ui_helpers as ui_helpers
from echofeed.common import config_info, api_request_classes as api_req_cls, \
    api_classes as api_cls


def home_page() -> None:
    if not app.storage.user.get('authenticated', False):
        return RedirectResponse('/login')

    response = requests.get(
        f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.GET]}",
        params={'user_id': app.storage.user.get("username", "")}
    )

    if response.status_code != 200:
        ui.notify('Failed to fetch user information', color='negative')
        return

    user = response.json().get('user_info', {})
    liked_articles = user.get('liked_articles', [])
    trending_articles = []

    for article_id in liked_articles:
        article_response = requests.get(
            f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.ARTICLE][config_info.AcceptedOperations.GET]}",
            params={'article_id': article_id}
        )
        if article_response.status_code != 200:
            continue

        article_info = article_response.json().get('article_info', {})
        if article_info:
            trending_articles.append(article_info)

    with ui.column().classes('items-center w-full mx-auto my-8'):
        ui.markdown(
            f"Hello, **{app.storage.user.get('username', '')}**!").classes('text-3xl')
        with ui.carousel(animated=True, arrows=True, navigation=True).classes('w-2/3 h-1/3 flex-wrap justify-center rounded-lg'):
            for i in range(min(5, len(trending_articles))):
                article = trending_articles[i]
                if article:
                    with ui.carousel_slide().style('background-color: #d7e3f4').classes('items-center pb-16 pt-10'):
                        ui.label('Your highlights').classes('text-2xl')
                        ui.label(article.get('title', '')).classes(
                            'text-lg')
                        ui.label(article.get('content', '')).classes(
                            'text-sm')
                        ui.label(article.get('date', '')).classes(
                            'text-xs')
                        with ui.button(on_click=lambda
                                url=article.get('url',
                                                       ''): ui.navigate.to(
                            url, new_tab=True)).classes(
                            'mt-2 q-pa-md'):
                            ui.icon('open_in_new')
                            ui.label(' Read more')
        def on_click_search_news():
            ui.navigate.to('/search-news')

        ui.button('Dive into your news journey!', on_click=on_click_search_news).classes('text-2xl mt-16 rounded-full')

def login_page() -> None:
    def try_login():
        username_value = username.value
        password_value = password.value
        response = requests.get(
            f"{config_info.API_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.LOGIN]}",
            params={'username': username_value, 'password': password_value}
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('result', False):
                user_info = data.get('user_info', {})
                app.storage.user.update({
                    'username': username_value,
                    'authenticated': True,
                    'is_admin': user_info.get('is_admin', False)
                })
                ui.notify('Login successful', color='positive')
                ui.navigate.to(app.storage.user.get('referrer_path', '/'))
            else:
                ui.notify('Wrong username or password', color='negative')
        else:
            ui.notify('Failed to connect to the server', color='negative')

    if app.storage.user.get('authenticated', False):
        return ui.navigate.to('/')

    with ui.card().classes('absolute-center items-center'):
        username = ui.input('Username').on('keydown.enter', try_login).classes(
            'w-full')
        password = ui.input('Password', password=True,
                            password_toggle_button=True).on('keydown.enter',
                                                            try_login).classes(
            'w-full')
        with ui.button('', on_click=try_login).classes('w-full'):
            ui.icon('login').classes('mr-2')
            ui.label('Log in')
        ui.label('Don\'t have an account?').classes('text-center').classes(
            'w-full')
        with ui.button('', on_click=lambda: ui.navigate.to('/register')).props('outline').classes('w-full'):
            ui.icon('person_add').classes('mr-2')
            ui.label('Register')


def register_page():
    def try_register():
        username_value = username.value
        last_name_value = last_name.value
        first_name_value = first_name.value
        birth_date_value = birth_date.value
        if birth_date_value == '':
            ui.notify('Please enter a valid birth date', color='negative')
            return
        try:
            birth_date_value = str(datetime.datetime.strptime(birth_date_value, '%Y-%m-%d').date())
        except ValueError:
            ui.notify('Birth date is not in the correct format (YYYY-MM-DD)',
                      color='negative')
            return
        location_value = location.value
        if password.value != confirm_password.value:
            ui.notify('Passwords do not match', color='negative')
            return
        password_value = password.value

        new_user_info = api_cls.User(
            username=username_value,
            first_name=first_name_value,
            last_name=last_name_value,
            birthday=birth_date_value,
            location=location_value,
            interests=[],
            viewed_articles=[],
            liked_articles=[],
            is_admin=False,
            password=password_value
        )
        request = api_req_cls.CreateUserRequest(user_info=new_user_info)

        response = requests.post(
            f"{ui_helpers.API_BASE_URL}{config_info.AcceptedOperations.ROUTES[config_info.Entity.USER][config_info.AcceptedOperations.CREATE]}",
            json=request.dict()
        )
        if response.status_code == 200:
            ui.notify('Registration successful', color='positive')
            time.sleep(2)
            ui.navigate.to('/login')
        else:
            ui.notify('Username already taken', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')

    with ui.card().classes('absolute-center py-10 my-10 w-2/5'):
        ui.label('Registration').classes('text-2xl text-center w-full')
        username = ui.input('Username').classes('w-full')
        password = ui.input('Password', password=True,
                            password_toggle_button=True).classes('w-full')
        confirm_password = ui.input('Confirm Password', password=True,
                                    password_toggle_button=True).classes(
            'w-full')
        last_name = ui.input('Last Name').classes('w-full')
        first_name = ui.input('First Name').classes('w-full')
        birth_date = ui.input('Birthdate').classes('w-full')
        with birth_date.add_slot('append'):
            ui.icon('edit_calendar').on('click', lambda: menu.open()).classes(
                'cursor-pointer')
            with ui.menu().props(
                    'position-anchor="bottom right" anchor="top left"') as menu:
                ui.date().bind_value(birth_date)
        location = ui.input('Location').classes('w-full')
        with ui.button('', on_click=try_register).classes('w-full'):
            ui.icon('person_add').classes('mr-2')
            ui.label('Register')
        ui.label('Already have an account?').classes('text-center').classes(
            'w-full')
        with ui.button('', on_click=lambda: ui.navigate.to('/login')).props('outline').classes('w-full'):
            ui.icon('login').classes('mr-2')
            ui.label('Log in')