# Import the required modules.
import logging
from fastapi import FastAPI, Form, HTTPException, Request, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from passlib.context import CryptContext
from .database import MongoDB
import os
from pydantic import BaseModel


# Get the environment variables.
mongodb_url = os.getenv("MONGODB_URL")
omdb_api_key = os.getenv("OMDB_API_KEY")

# Create the FastAPI app.
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.DEBUG)

# Dependencies
mongodb = MongoDB(mongodb_url)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

# Models
class UpdateMovieCategory(BaseModel):
    category: str

class UpdateMovieRating(BaseModel):
    rating: int

class SearchQuery(BaseModel):
    query: str

# Dependency functions
def get_mongodb() -> MongoDB:
    """Return an instance of the MongoDB class."""
    return mongodb

# Helper functions
async def omdb_search(search_term: str, page_number: int)->tuple[bool, list[dict[str, str]]]:
    """Fetches movies from the OMDb API based on the provided search term and page number."""
    
    # Create the URL and parameters for the request.
    url = "http://www.omdbapi.com/"
    params = {"apikey": omdb_api_key, "s": search_term, "type": "movie", "r": "json","page": page_number}

    # Send the request using the httpx module.
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

        # If the request was successful, return the movies.
        if "Search" in data:
            return (True, data["Search"])
        # Otherwise, return an empty list.
        else:
            return (False, [])

async def get_movies(query: str) -> list[dict[str, str]]:
    """Fetches movies from the OMDB API based on the provided query."""    
    
    # Initialize variables.
    flag = True
    page = 1
    movies= []
    
    # Loop until any number of movies are fetched or 10 pages are reached.
    while flag and page < 11: 
        data= await omdb_search(query, page)
        if data[0]:
            movies.extend(data[1])
            page+=1
        else:
            flag=False
    
    # If no movies from OMDB API, get movies from MongoDB.
    if not movies:
        movies= mongodb.get_movies_by_title(query)

    return movies

def save_movies(movies: list[dict[str, any]], random: bool) -> None:
    """Saves movies to MongoDB."""
    
    for movie in movies:
        # The IMDB ID is used as the key in MongoDB.
        imdb_id = movie["imdbID"]
        
        # Save the movie to MongoDB.
        mongodb.add_movie(imdb_id, random)

async def fetch_random_movies(word=""):
    """ Fetches movies from the OMDB API using random word-page pairs from MongoDB."""
    
    # Delete word from MongoDB if no movies are found.
    if word: mongodb.delete_word(word)
    
    # Return if no words are left in MongoDB.
    if mongodb.get_words_count() == 0: return

    # Get random word-page pair from MongoDB.
    random = mongodb.get_random_word_page()

    # Assign word and page from random word-page pair.
    word = random['word']
    page = random['page']

    # Loop until any number of movies are fetched.
    while mongodb.movies_collection.count_documents({}) < 2000:
        # Fetch movies from OMDB API.
        data = await omdb_search(word, page)
        # If movies are fetched, save them to MongoDB.
        if data[0]:
            movies = data[1]
            # Create movie in MongoDB.
            save_movies(movies, True)
            # Increment page and update MongoDB.
            page += 1
            mongodb.update_page(word, page)
    return

async def get_current_user_id(request: Request):
    """Gets the current user ID from the cookies."""
    user_id = request.cookies.get("user_id")
    return user_id


#Home page
@app.get("/")
async def home_page(request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Handles the GET request and renders the home.html template."""
    
    # Fetches 15 movies from the database and sorts them by their release date.
    movies = list(mongodb.movies_collection.find().sort("Released", -1).limit(15))

    # Fetches 15 random movies from the database.
    random_movies= mongodb.get_random_movies(15)

    # Checks if a user is logged in.
    current_user = None
    current_user_movies = []
    
    # If a user is logged in, fetches their details and their list of movies.
    if current_user_id:
        current_user = mongodb.get_user_by_id(current_user_id)
        current_user_movies = [mongodb.retrieve_movie_details(movie["imdbID"]) for movie in current_user["list"]]

    # Fetches the top 3 users from the leaderboard.
    leaderboard= mongodb.get_leaderboard()[0:3]
    if not leaderboard:
        leaderboard = []

    return templates.TemplateResponse("home.html", {"request": request, "movies": movies,"r_movies":random_movies,
                                                     "current_user": current_user, "current_user_movies": current_user_movies,
                                                      "leaderboard": leaderboard})

    
#Movie page
@app.get("/movie/{imdb_id}")
async def movie_page(imdb_id: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Renders the movie.html template for the specified IMDb ID."""

    # Get the movie details from the database.
    movie_data = mongodb.retrieve_movie_details(imdb_id)

    # Create a new movie if one doesn't exist yet.
    if not movie_data:
        mongodb.add_movie(imdb_id)
        movie_data = mongodb.retrieve_movie_details(imdb_id)

    # Get the current user if there is one.
    current_user = None
    if current_user_id:
        current_user = mongodb.get_user_by_id(current_user_id)

    # Get the reviews for the movie.
    reviews = mongodb.get_movie_reviews(imdb_id)
    if reviews:
        reviews = reviews["reviews"]
    else:
        reviews = []

    # Get the user's review for the movie if there is one.
    user_review = mongodb.get_movie_review(imdb_id, current_user_id)
    if not user_review:
        user_review = {}
    
    # If the user has reviewed the movie, remove their review from the list of reviews.
    else:
        user_review = user_review["reviews"][0]
        reviews.remove(user_review)

    return templates.TemplateResponse("movie.html",{"request": request, "movie": movie_data, 
                                                    "current_user": current_user, "reviews": reviews, "user_review": user_review})


@app.post("/movie/{imdb_id}")
async def process_movie(imdb_id: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Processes the movie form and adds the movie to the user's list."""
    
    # Get the form data.
    form = await request.form()
    action = form.get("action")

    # If user is adding a movie to their list.
    if action == "add":
        category = form.get("category")
        rating= form.get("rating") if form.get("rating") else -1

        # If user is logged in.
        if current_user_id:
            # Get the movie details from the database.
            movie_data = mongodb.retrieve_movie_details(imdb_id)

            # Create a new movie if one doesn't exist in movie list.
            if movie_data:
                add_movie_data = {"imdbID": movie_data["imdbID"], "Title": movie_data["Title"],"Poster": movie_data["Poster"],
                                  "Status": category,"Rating": int(rating),}
                mongodb.add_movie_to_list(current_user_id, add_movie_data)

    # If user is deleting a movie from their list.
    elif action == "delete":
        if current_user_id:
            mongodb.remove_movie_from_list(current_user_id, imdb_id)

    # If user is updating a movie in their list.
    elif action == "update":
        category = form.get("category")
        rating= form.get("rating") if form.get("rating") else 0
        if current_user_id:

            # Update movie category and rating.
            mongodb.update_movie_category(current_user_id, imdb_id, category)
            mongodb.update_movie_rating(current_user_id, imdb_id, int(rating))

            # If user has reviewed the movie, update the review.
            if mongodb.get_movie_review(imdb_id, current_user_id):
                mongodb.update_movie_reviews_review(imdb_id, current_user_id, int(rating))
                mongodb.update_movie_reviews_category(imdb_id, current_user_id, category)
    
    else:
        return RedirectResponse(f"/movie/{imdb_id}", status_code=303)


    return RedirectResponse(f"/movie/{imdb_id}", status_code=303)


#Search page
@app.get("/search")
async def search_movies(query: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Searches movies based on the provided query and renders the search.html template."""
    
    # Get movies from the API.
    movies = await get_movies(query)

    # Get the current user if there is one.
    current_user = None
    if current_user_id:
        current_user = mongodb.get_user_by_id(current_user_id)

    return templates.TemplateResponse("search.html", {"request": request, "movies": movies, "current_user": current_user})


#Random page
@app.get("/random")
async def random_movies(request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Renders the random.html template."""

    # Get the random movies from the database.
    movies = mongodb.get_random_movies(18)

    # Get the current user if there is one.
    current_user = None
    if current_user_id:
        current_user = mongodb.get_user_by_id(current_user_id)

    return templates.TemplateResponse("random.html", {"request": request, "movies": movies, "current_user": current_user})


#Movie list
@app.get("/movielist/{username}")
async def movie_list(username: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Renders the movie_list.html template for the specified username."""
    
    # Get the user from the database.
    current_user = mongodb.get_user_by_username(username)

    # If the user doesn't exist, return a 404 error.
    if not current_user:
        return RedirectResponse("/", status_code=status.HTTP_404_NOT_FOUND)

    # Get the movies in the user's list.
    movies = current_user["list"] if current_user else []

    return templates.TemplateResponse("movie_list.html", {"request": request, "current_user_id":current_user_id, "current_user":  current_user, "movies": movies})

# Update the movie category in the database.
@app.put("/movielist/api/{user_id}/movie/{imdb_id}/status", name="update_movie_status")
async def update_movie_category(user_id: str,imdb_id: str,category: UpdateMovieCategory,mongodb: MongoDB = Depends(get_mongodb)):
    """Updates the category of a movie in the user's list."""

    mongodb.update_movie_category(user_id, imdb_id, category.category)

    # If the user has reviewed the movie, update the review.
    if mongodb.get_movie_review(imdb_id, user_id):
        mongodb.update_movie_reviews_category(imdb_id, user_id, category.category)
        
    return {"message": "Movie category updated successfully."}

@app.put("/movielist/api/{user_id}/movie/{imdb_id}/rating", name="update_movie_rating")
async def update_movie_rating(user_id: str,imdb_id: str,rating: UpdateMovieRating,mongodb: MongoDB = Depends(get_mongodb)):
    """Updates the rating of a movie in the user's list."""

    mongodb.update_movie_rating(user_id, imdb_id, int(rating.rating))
    
    # If the user has reviewed the movie, update the review.
    if mongodb.get_movie_review(imdb_id, user_id):
        mongodb.update_movie_reviews_review(imdb_id, user_id, int(rating))

    return {"message": "Movie rating updated successfully."}

@app.get("/movielist/api/{user_id}/search")
async def search_movies(user_id: str, query: str, mongodb: MongoDB = Depends(get_mongodb)):
    """Fetches the search results for the given query."""
    
    # Get the movies in the user's list that match the query.
    movies = mongodb.search_movies_by_title_in_list(user_id, query)
    
    return {"movies": movies}

@app.get("/movielist/api/{user_id}/sort")
async def sort_movies(user_id: str, filter: str, mongodb: MongoDB = Depends(get_mongodb)):
    """Sorts the movie list based on the given filter."""
    
    # Get the movies in the user's list sorted by the given filter.
    sorted_movies = mongodb.sort_movies_in_list(user_id, filter)

    return {"movies": sorted_movies}


#User profile
@app.get("/register")
async def register(request: Request):
    """Renders the register.html template."""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def process_registration(request: Request):
    """Processes the registration form and adds a new user to the database."""

    # Get the form data
    form = await request.form()
    username = form.get("username")
    
    # Get the password and confirm password from the form.
    password = form.get("password")
    confirm_password = form.get("confirm_password")
    avatar = form.get("avatar")

    # Validate the form data.
    error_messages = []
    if not avatar:
        error_messages.append("Please choose an avatar")
    if password != confirm_password:
        error_messages.append("Passwords do not match")
    if mongodb.get_user_by_username(username):
        error_messages.append("Username already exists")
    if error_messages:
        return templates.TemplateResponse("register.html", {"request": request, "error_messages": error_messages})

    # Add the user to the database.
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

    # Get the user from the database.
    user = mongodb.get_user_by_username(username)

    # If the user doesn't exist or the password is incorrect, return an error message.
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        error_message = "Invalid username or password"
        return templates.TemplateResponse("login.html", {"request": request, "error_message": error_message})

    # If the user exists and the password is correct, set a cookie with the user ID and redirect to the home page.
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=str(user["_id"]))
    return response

@app.route("/logout", methods=["GET", "POST"])
async def logout(request: Request):
    """Logs out the user by deleting the user ID cookie."""

    # Delete the user ID cookie and redirect to the home page.
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="user_id")
    return response

#Reviews
@app.get("/review/{imdb_id}")
async def submit_review(imdb_id: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """ Renders the submit_review.html template for the specified IMDb ID."""
    
    # If the user is not logged in, redirect to the login page.
    if not current_user_id:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Get the current user's data, and the data for the movie being reviewed.
    current_user = mongodb.get_user_by_id(current_user_id)
    movie_data = mongodb.retrieve_movie_details(imdb_id)

    #  Create a new movie if one doesn't exist yet.
    if not movie_data:
        mongodb.add_movie(imdb_id)
        movie_data = mongodb.retrieve_movie_details(imdb_id)

    # Get the user's review for the movie if there is one.
    review = mongodb.get_movie_review(imdb_id, current_user_id)
    if not review:
        review = {}
    else:
        review = review["reviews"][0]

    return templates.TemplateResponse("review.html", {"request": request, "movie": movie_data, "user_id": current_user_id, "review": review, "current_user": current_user})

@app.post("/process-review/{imdb_id}")
async def process_review(imdb_id: str, request : Request, current_user_id: str = Depends(get_current_user_id)):
    """ Processes the review submission for the specified IMDb ID."""
    
    # If the user is not logged in, redirect to the login page.
    if not current_user_id:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Get the current user's data.
    current_user = mongodb.get_user_by_id(current_user_id)
    
    # Get the movie data from the database.
    movie_data = mongodb.retrieve_movie_details(imdb_id)
    if not movie_data:
        mongodb.add_movie(imdb_id)
        movie_data = mongodb.retrieve_movie_details(imdb_id)

    # Get the review from the form.
    review=await request.form()

    # If the user has submitted a review, add it to the database.
    if review:
        rating= int(review["rating"])
        recommend= True if review["recommend"] == "on" else False

        # If the user has already reviewed the movie, update the review.
        if mongodb.get_movie_review(imdb_id, current_user_id):
            mongodb.update_movie_review(imdb_id, current_user_id, review["status"], rating, recommend, review["review"])
            mongodb.update_movie_rating(current_user_id, imdb_id, rating)
            mongodb.update_movie_category(current_user_id, imdb_id, review["status"])
        
        # Otherwise, add the review to the database.
        else:
            mongodb.add_movie_review(imdb_id, current_user_id, review["status"], rating, recommend, review["review"], current_user["username"], current_user["avatar"])

            # If the user has already added the movie to their list, update the movie's rating and category.
            if mongodb.get_movie_in_list(imdb_id, current_user_id):
                mongodb.update_movie_rating(current_user_id, imdb_id, rating)
                mongodb.update_movie_category(current_user_id, imdb_id, review["status"])
            
            # Otherwise, add the movie to the user's list.
            else:
                movie_dict = { "imdbID": movie_data["imdbID"], "Title": movie_data["Title"], "Poster": movie_data["Poster"], "Status": review["status"], "Rating": rating}
                mongodb.add_movie_to_list(current_user_id, movie_dict)

    # If the user has not submitted a review, delete their review from the database.
    else:
        mongodb.delete_movie_review(imdb_id, current_user_id)

    return RedirectResponse(url=f"/review/{imdb_id}", status_code=status.HTTP_303_SEE_OTHER)

#Game 
@app.get("/game")
async def game_intro(request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Renders the game_intro.html template."""

    # Get the leaderboard from the database.
    leaderboard = mongodb.get_leaderboard()
    if not leaderboard:
        leaderboard = []

    # Get the current user from the database.
    current_user= mongodb.get_user_by_id(current_user_id)

    return templates.TemplateResponse("game_intro.html", {"request": request, "leaderboard": leaderboard, "game_over": False, "current_user": current_user})

@app.get("/start_game")
async def start_game(request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Starts a new game and redirects to the game page."""

    # Get two random movies from the database.
    movies = mongodb.get_random_movies(2, True)
    
    # Get the current user from the database.
    user=mongodb.get_user_by_id(current_user_id)
    
    # Get the base and hidden movies.
    base_movie = movies[0]
    hidden_movie = movies[1]
    
    # Make sure the hidden movie has a different IMDB rating than the base movie.
    while hidden_movie["imdbRating"] == base_movie["imdbRating"]:
        hidden_movie = mongodb.get_random_movies(game=True)[0]
    
    # Create a new game in the database.
    game_data = {
                "base_movie_id": base_movie["imdbID"],
                "base_movie_imdb_rating": base_movie["imdbRating"],
                "hidden_movie_id": hidden_movie["imdbID"],
                "hidden_movie_imdb_rating": hidden_movie["imdbRating"],
                "num_lives": 3,
                "score": 0,
                "movie_list": [base_movie["imdbID"], hidden_movie["imdbID"]]
                }
    game_id = mongodb.create_game(game_data)
    
    # Add the user to the leaderboard if they are not already on it.
    if not mongodb.get_user_score(user["username"]):
        mongodb.add_user_to_leaderboard(user["username"], user["avatar"])

    return RedirectResponse(f"/game/{game_id}")

@app.get("/game/{game_id}")
async def game(request: Request, game_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Renders the game.html template for the specified game ID."""
    
    # Get the game data from the database.
    game_data = mongodb.get_game(game_id)

    # Get the base and hidden movies.
    base_movie = mongodb.retrieve_movie_details(game_data["base_movie_id"])
    hidden_movie = mongodb.retrieve_movie_details(game_data["hidden_movie_id"])
    
    # Get the score from the game data.
    score= game_data["score"]
    
    return templates.TemplateResponse("game.html", {"request": request, "game_id": game_id,
                                                     "base_movie": base_movie, "hidden_movie": hidden_movie, 
                                                     "num_lives": game_data["num_lives"], "score": score})

@app.post("/game/{game_id}")
async def process_game(request: Request, game_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Processes the game form and updates the game data in the database."""
    
    # Get the form data.
    form = await request.form()
    chosen_movie_id = form.get("chosen_movie_id")
    
    # Get the game data from the database.
    game_data = mongodb.get_game(game_id)
    
    # Get the base and hidden movies.
    base_movie = {"imdbID":game_data["base_movie_id"], "imdbRating":game_data["base_movie_imdb_rating"]}
    hidden_movie = {"imdbID":game_data["hidden_movie_id"], "imdbRating":game_data["hidden_movie_imdb_rating"]}
    
    # Determine which movie the user has chosen.
    chosen_movie = base_movie if chosen_movie_id == base_movie["imdbID"] else hidden_movie

    # Determine if the user's chosen movie is the correct movie.
    if base_movie["imdbRating"] <= hidden_movie["imdbRating"]:
        is_correct = chosen_movie == hidden_movie   
    else:
        is_correct = chosen_movie == base_movie
    
    # If the user's chosen movie is not the correct movie, decrement the number of lives.
    if not is_correct:
        game_data["num_lives"] -= 1

        # If the user has no lives left, redirect to the game over page.
        if game_data["num_lives"] < 1:
            return await game_over(request, game_id, current_user_id)

        
    # If the user's chosen movie is the correct movie, increment the score.
    else:
        # Update the game's scoreboard.
        game_data["score"] += 1
    
    # Get the score from the game data.
    score = game_data["score"] 

    # Update the game's base movie.
    game_data["base_movie_id"],game_data["base_movie_imdb_rating"] = hidden_movie["imdbID"], hidden_movie["imdbRating"]

    # Get a new hidden movie.
    base_movie = mongodb.retrieve_movie_details(game_data["base_movie_id"])
    hidden_movie = mongodb.get_random_movies(for_game=True)[0]

    # Make sure the hidden movie has a different IMDB rating than the base movie.
    while hidden_movie["imdbID"] not in game_data["movie_list"] and hidden_movie["imdbRating"] == base_movie["imdbRating"]:
        hidden_movie = mongodb.get_random_movies(for_game=True)[0]

    # Update the game's hidden movie.
    game_data["hidden_movie_id"],game_data["hidden_movie_imdb_rating"] = hidden_movie["imdbID"], hidden_movie["imdbRating"]
    game_data["movie_list"].append(hidden_movie["imdbID"])

    # Update the game data in the database.
    mongodb.update_game(game_id, game_data)
    
    return templates.TemplateResponse("game.html", {"request": request, "game_id": game_id, "base_movie": base_movie, 
                                                    "hidden_movie": hidden_movie, "num_lives": game_data["num_lives"], 
                                                    "is_correct": is_correct, "score": score})

@app.route("/game_over/{game_id}", methods=["GET", "POST"])
async def game_over(request: Request, game_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Renders the game_over.html template for the specified game ID."""
    
    # Get the game data from the database.
    game = mongodb.get_game(game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Get the current user from the database.
    user = mongodb.get_user_by_id(current_user_id)
    
    # Get the user's score and previous score.
    user_score = game["score"]
    old_score = mongodb.get_user_score(user["username"])["score"] if mongodb.get_user_score(user["username"]) else -1
    
    # Update the user's score if it is higher than their previous score.
    better = False
    if user_score > old_score:
        mongodb.update_leaderboard(user["username"], game["score"])
        better = True        
    leaderboard = mongodb.get_leaderboard()

    # Get the user's rank.
    try:
        rank = next(i + 1 for i, item in enumerate(leaderboard) if item["username"] == user["username"])
    except StopIteration:
        rank = 0


    # If the user's rank is in the top 3, set the better variable to True.
    if leaderboard[2]["score"] < user_score: better = True

    return templates.TemplateResponse("game_intro.html", {"request": request, "user_score": user_score, "rank": rank, 
                                                         "leaderboard": leaderboard , "game_over": True, "better": better,
                                                         "current_user": user})
  
