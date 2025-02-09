from nicegui import Client, app
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

unrestricted_page_routes = ['/login', '/register']


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware pentru restricționarea accesului la paginile protejate."""

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path
                return RedirectResponse('/login')
        return await call_next(request)
