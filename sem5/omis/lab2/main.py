from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import logging
from src.control import AuthManager, RegistarationManager

def get_logger(filename: str = None) -> logging.Logger:
    if not filename:
        filename = 'application.log'
    logger_ = logging.getLogger(filename)
    if not logger_.handlers:
        logger_.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(f"{filename}")
        file_handler.setLevel(logging.WARNING)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        logger_.addHandler(file_handler)
        logger_.addHandler(stream_handler)
    return logger_


logger = get_logger()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="secret_key")

templates = Jinja2Templates(directory="src/view")

auth_manager = AuthManager()
reg_manager = RegistarationManager()

user = []

def is_authenticated(request: Request):
    return "user" in request.session

@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    logger.info("GET /")
    if auth_manager.is_authenticated(request):
        logger.info("User authenticated")
        return RedirectResponse(url="/menu", status_code=status.HTTP_303_SEE_OTHER)
    logger.info("User NOT authenticated")
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/register")
@auth_manager.logout_required
async def register(request: Request):
    logger.info("GET Register")
    return templates.TemplateResponse("registration.html", {"request": request})


@app.post("/register", response_class=RedirectResponse)
async def register_post(request: Request):
    logger.info("POST Register")
    form_data = await request.form()
    login = form_data.get("login")
    password = form_data.get("password")
    dob = form_data.get("dob")
    role = form_data.get("role")

    if not login or not password or not dob or not role:
        raise HTTPException(status_code=400, detail="Все поля обязательны для заполнения.")

    try:
        reg_manager.create_user(login, password, dob, role)
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    except HTTPException as e:
        raise e


@app.get("/login")
@auth_manager.logout_required
async def login(request: Request):
    logger.info("GET Login")
    return templates.TemplateResponse("auth.html", {"request": request})


@app.post("/login", response_class=RedirectResponse)
async def login_post(request: Request):
    logger.info("POST Login")
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    
    logger.info("Username: %s", username)
    logger.info("Password: %s", password)

    if username == "client" and password == "helloworld":
        auth_manager.login(request, username)
        return RedirectResponse(url="/menu", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")


@app.get("/menu")
@auth_manager.login_required
async def menu(request: Request):
    logger.info("GET Menu")
    return templates.TemplateResponse("client.html", {"request": request})


@app.get("/logout")
async def logout(request: Request):
    logger.info("GET Logout")
    auth_manager.logout(request)
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
