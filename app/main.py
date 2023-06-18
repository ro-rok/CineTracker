import logging
import random
from fastapi import FastAPI, Form, Request, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from passlib.context import CryptContext
from .database import MongoDB


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.DEBUG)

mongodb = MongoDB("mongodb+srv://rk868:hM86hlQU1F60GVBa@movie.qxbfjsl.mongodb.net/")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()


async def get_current_user_id(request: Request):
    user_id = request.cookies.get("user_id")
    return user_id


async def fetch_random_movies():
    """Fetches 20 random movies from the OMDb API and stores them in the database."""
    movies_count = mongodb.movies_collection.count_documents({})
    while movies_count < 21:
        imdb_id = f"tt{random.randint(0, 9999999)}"
        mongodb.create_movie(imdb_id, True)


@app.get("/")
async def read_root(request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Reads the root route and renders the index.html template."""
    
    await fetch_random_movies()

    movies = list(mongodb.movies_collection.find().sort("Released", -1).limit(15))

    current_user = None
    if current_user_id:
        current_user = mongodb.get_user_by_id(current_user_id)

    return templates.TemplateResponse("index.html", {"request": request, "movies": movies, "current_user": current_user})


@app.get("/movie/{imdb_id}")
async def movie_page(imdb_id: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Renders the movie.html template for the specified IMDb ID."""
    movie_data = mongodb.retrieve_movie_details(imdb_id)

    if not movie_data:
        mongodb.create_movie(imdb_id)
        movie_data = mongodb.retrieve_movie_details(imdb_id)

    current_user = None
    if current_user_id:
        current_user = mongodb.get_user_by_id(current_user_id)

    return templates.TemplateResponse("movie.html", {"request": request, "movie": movie_data, "current_user": current_user})


@app.get("/search")
async def search_movies(query: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Searches movies based on the provided query and renders the search.html template."""
    base_url = "http://www.omdbapi.com/"
    api_key = "1a8d2b0d"

    params = {"apikey": api_key, "s": query, "type": "movie", "r": "json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        data = response.json()

    movies = data.get("Search", [])

    current_user = None
    if current_user_id:
        current_user = mongodb.get_user_by_id(current_user_id)

    return templates.TemplateResponse("search.html", {"request": request, "movies": movies, "current_user": current_user})


@app.get("/register")
async def register(request: Request):
    """Renders the register.html template."""
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def process_registration(request: Request):
    """Processes the registration form and adds a new user to the database."""
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    confirm_password = form.get("confirm_password")
    avatar = form.get("avatar")
    error_messages = []

    if not avatar:
        error_messages.append("Please choose an avatar")

    if password != confirm_password:
        error_messages.append("Passwords do not match")

    if mongodb.get_user_by_username(username):
        error_messages.append("Username already exists")

    if error_messages:
        return templates.TemplateResponse("register.html", {"request": request, "error_messages": error_messages})

    user_id = mongodb.add_user(username, password, avatar)
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=user_id)
    return response


@app.get("/login")
async def login(request: Request):
    """Renders the login.html template."""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def process_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Processes the login form and sets the user ID in a cookie upon successful login."""
    logging.info(f"Username: {username}")
    user = mongodb.get_user_by_username(username)
    if not user:
        logging.info(f"User '{username}' not found")
        error_message = "Invalid username or password"
        return templates.TemplateResponse("login.html", {"request": request, "error_message": error_message})

    if not pwd_context.verify(password, user["hashed_password"]):
        logging.info(f"Invalid password for user '{username}'")
        error_message = "Invalid username or password"
        return templates.TemplateResponse("login.html", {"request": request, "error_message": error_message})

    logging.info(f"Successful login for user '{username}'")
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=str(user["_id"]))
    return response


@app.route("/logout", methods=["GET", "POST"])
async def logout(request: Request):
    """Logs out the user by deleting the user ID cookie."""
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="user_id")
    return response


@app.get("/forgot-password")
async def forgot_password(request: Request):
    """Renders the forgot_password.html template."""
    return templates.TemplateResponse("forgot_password.html", {"request": request})


@app.get("/submit-review/{imdb_id}")
async def submit_review(imdb_id: str, request: Request, user_id: str = Depends(get_current_user_id)):
    """Renders the submit_review.html template for the specified IMDb ID."""
    if not user_id:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    movie_data = mongodb.retrieve_movie_details(imdb_id)

    if not movie_data:
        mongodb.create_movie(imdb_id)
        movie_data = mongodb.retrieve_movie_details(imdb_id)

    return templates.TemplateResponse(
        "submit_review.html", {"request": request, "movie": movie_data, "user_id": user_id}
    )


@app.post("/submit-review/{imdb_id}")
async def process_review(imdb_id: str, review: str, request: Request, user_id: str = Depends(get_current_user_id)):
    """Processes the review form and updates the movie review in the database."""
    if not user_id:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    mongodb.update_movie_review(imdb_id, user_id, review)
    return RedirectResponse(url=f"/movie/{imdb_id}", status_code=status.HTTP_302_FOUND)
