from fastapi import Request, status
from fastapi.responses import RedirectResponse


class AuthManager:
    def __init__(self, session_key: str = "user"):
        self.session_key = session_key

    def is_authenticated(self, request: Request) -> bool:
        return self.session_key in request.session

    def login(self, request: Request, username: str):
        request.session[self.session_key] = username

    def logout(self, request: Request):
        request.session.clear()

    def login_required(self, func):
        async def wrapper(request: Request):
            if not self.is_authenticated(request):
                return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
            return await func(request)
        return wrapper

    def logout_required(self, func):
        async def wrapper(request: Request):
            if self.is_authenticated(request):
                return RedirectResponse(url="/menu", status_code=status.HTTP_303_SEE_OTHER)
            return await func(request)
        return wrapper
