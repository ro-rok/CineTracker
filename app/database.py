# Description: This file contains the database class that is used to interact with the MongoDB database.

# Import statements
import pymongo
import requests
from datetime import datetime
from passlib.hash import bcrypt
from bson import ObjectId


# Database class
class MongoDB:
    def __init__(self, url: str):
        """Initialize a database object and connect to MongoDB"""
        self.client = pymongo.MongoClient(url)
        self.db = self.client["movie_app"]
        self.movies_collection = self.db["movies"]
        self.users_collection = self.db["user"]
        self.reviews_collection = self.db["reviews"]
        self.words_collection = self.db["words"]
        self.leaderboard_collection = self.db["leaderboard"]
        self.games_collection = self.db["games"]


    #Movies
    def add_movie(self, imdb_id: str, in_randomizer: bool = False) -> None:
        """Creates a movie document in the database."""

        # Skip adding duplicate movies
        if self.movies_collection.count_documents({"imdbID": imdb_id}) > 0:
            return

        # fetch data from API
        url1 = f"http://www.omdbapi.com/?i={imdb_id}&apikey=1a8d2b0d&plot=full"
        url2 = f"http://www.omdbapi.com/?i={imdb_id}&apikey=1a8d2b0d"

        # Fetch data from URL 1 and store it in a temporary dictionary.
        response1 = requests.get(url1).json()
        temp = response1

        # Check if the movie is in the randomizer and skip if it is not.
        if in_randomizer:
            try:
                # Check for errors 
                if temp["Response"]=="False" or temp["Runtime"] =="N/A" or temp["Poster"]=="N/A" or temp["imdbRating"] == "N/A" or temp["Director"]=="N/A" or temp["Released"]=="N/A":
                    return
            except KeyError as e:
                print("Invalid key:", e)
                return

        # Convert data types and rename fields for consistency with the database schema.
        temp["Plot_l"] = temp.pop("Plot")
        temp["Released"] = datetime.strptime(temp.pop("Released"), "%d %b %Y")
        temp["Year"] = int(temp.pop("Year"))
        temp["imdbRating"] = float(temp.pop("imdbRating"))
        temp["imdbVotes"] = int(temp.pop("imdbVotes").replace(",", ""))

        # Fetch data from URL 2 and add it to the temp dictionary.
        response2 = requests.get(url2).json()
        temp["Plot_s"] = response2["Plot"]

        # Store the movie data in the database collection.
        self.movies_collection.insert_one(temp)



    def retrieve_movie_details(self, imdb_id: str) -> dict:
        """Retrieves a movie document from the database."""
        return self.movies_collection.find_one({"imdbID": imdb_id})

    def get_random_movies(self, num_movies=1, for_game = False) -> list:
        """Returns a list of random movies from the database."""
        
        # Check if the movies are for the game. 
        if for_game:

            # Get movies with imdbVotes greater than 60000 or with Oscar awards.
            imdbVotes = 60000
            movies = self.movies_collection.aggregate([
                {"$match": {"$or": [{"imdbVotes": {"$gt": imdbVotes}}]}},
                {"$sample": {"size": num_movies}}
            ])

        # Get random movies from the database collection.     
        else:
            movies = self.movies_collection.aggregate([
                {"$sample": {"size": num_movies}}
            ])

        return list(movies)

    def get_movies_by_title(self, search_term: str) -> list:
        """Returns a list of movies from the database that match the given search term."""
        result = self.movies_collection.find({"Title": {"$regex": search_term, "$options": "i"}})
        return list(result)
    
    #Users
    def add_user(self, username: str, password: str, avatar: str) -> str:
        """Creates a user document in the database."""
        hashed_password = bcrypt.hash(password)
        user_id = str(self.users_collection.insert_one({"username": username, "hashed_password": hashed_password, "avatar": avatar, "list":[]}).inserted_id)
        return user_id

    def get_user_by_username(self, username: str) -> dict:
        """Returns a user from the database."""
        return self.users_collection.find_one({"username": username})

    def get_user_by_id(self, user_id: str) -> dict:
        """Returns a user from the database."""
        return self.users_collection.find_one({"_id": ObjectId(user_id)})

    #Movie list
    def add_movie_to_list(self, user_id: str, movie_data: dict) -> None:
        """Adds a movie to the user's list."""
        self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"list": movie_data}},
        )

    def get_movie_in_list(self, user_id: str, imdb_id: str) -> dict:
        """Returns a movie from the user's list."""
        result = self.users_collection.aggregate([
            {"$match": {"_id": ObjectId(user_id)}},
            {"$unwind": "$list"},
            {"$match": {"list.imdbID": imdb_id}},
            {"$project": {"_id": 0, "list": 1}},
        ])

        return result.next() if result else None

    def remove_movie_from_list(self, user_id: str, imdb_id: str) -> None:
        """Removes a movie from the user's list."""
        self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"list": {"imdbID": imdb_id}}},
        )

    def update_movie_category(self, user_id: str, imdb_id: str, category: str) -> None:
        """Updates the category of a movie in the user's list."""
        self.users_collection.update_one(
            {"_id": ObjectId(user_id), "list.imdbID": imdb_id},
            {"$set": {"list.$.Status": category}},
        )

    def update_movie_rating(self, user_id: str, imdb_id: str, rating: int) -> None:
        """Updates the rating of a movie in the user's list."""
        self.users_collection.update_one(
            {"_id": ObjectId(user_id), "list.imdbID": imdb_id},
            {"$set": {"list.$.Rating": rating}},
        )

    def search_movies_by_title_in_list(self, user_id: str, search_term: str) -> list:
        """Searches for movies in the user's list by title."""
        results = self.users_collection.aggregate([
            {"$match": {"_id": ObjectId(user_id)}},
            {"$unwind": "$list"},
            {"$match": {"list.Title": {"$regex": search_term, "$options": "i"}}},
            {"$project": {"_id": 0, "list": 1}},
        ])

        movies = []
        for result in results:
            movies.append(result['list'])

        return movies

    def sort_movies_in_list(self, user_id: str, filter: str) -> list:
        """Sorts the movies in the user's list based on the given filter."""

        # Get the list of movies from the user
        user = self.get_user_by_id(user_id)
        if user:
            movies = user["list"]
        else:
            movies = []

        # Sort the list of movies
        if filter == "alphabetical_asc":
            sorted_movies = sorted(movies, key=lambda x: x["Title"], reverse=False)
        elif filter == "alphabetical_desc":
            sorted_movies = sorted(movies, key=lambda x: x["Title"], reverse=True)
        elif filter == "rating_asc":
            sorted_movies = sorted(movies, key=lambda x: x["Rating"], reverse=False)
        elif filter == "rating_desc":
            sorted_movies = sorted(movies, key=lambda x: x["Rating"], reverse=True)
        else:
            sorted_movies = movies

        return sorted_movies

    #Reviews
    def add_movie_review(self, imdb_id: str, user_id: str, status: str, rating: int, recommend: bool, review: str, username: str, avatar: str ) -> None:
        """Adds a review to the movie."""
        self.reviews_collection.update_one(
            {"imdbID": imdb_id},
            {
                "$push": {
                    "reviews": {
                        "user_id": user_id,
                        "status": status,
                        "rating": rating,
                        "recommend": recommend,
                        "review": review,
                        "username": username,
                        "avatar": avatar
                    }
                }
            },
            upsert=True
        )

    def update_movie_review(self, imdb_id: str, user_id: str, status: str, rating: int, recommend: bool, review: str) -> None:
        """Updates a review of the movie."""
        self.reviews_collection.update_one(
            {"imdbID": imdb_id, "reviews.user_id": user_id},
            {
                "$set": {
                    "reviews.$.status": status,
                    "reviews.$.rating": rating,
                    "reviews.$.recommend": recommend,
                    "reviews.$.review": review
                }
            }
        )

    def delete_movie_review(self, imdb_id: str, user_id: str) -> None:
        """Deletes a review of the movie."""
        self.reviews_collection.update_one(
            {"imdbID": imdb_id},
            {"$pull": {"reviews": {"user_id": user_id}}}
        )

    def get_movie_review(self, imdb_id: str, user_id: str) -> dict:
        """Returns a review of the movie."""
        return self.reviews_collection.find_one(
            {"imdbID": imdb_id, "reviews.user_id": user_id},
            {"reviews.$": 1}
        )

    def get_movie_reviews(self, imdb_id: str) -> dict:
        """Returns all reviews of the movie."""
        return self.reviews_collection.find_one({"imdbID": imdb_id})

    def update_movie_reviews_review(self, imdb_id: str, user_id: str, rating: int) -> None:
        """Updates the rating of a user in the movie reviews."""
        self.reviews_collection.update_one(
            {"imdbID": imdb_id, "reviews.user_id": user_id},
            {"$set": {"reviews.$.rating": rating}}
        )

    def update_movie_reviews_category(self, imdb_id: str, user_id: str, category: str) -> None:
        """Updates the status of a user in the movie reviews."""
        self.reviews_collection.update_one(
            {"imdbID": imdb_id, "reviews.user_id": user_id},
            {"$set": {"reviews.$.status": category}}
        )

    #Leaderboard
    def get_leaderboard(self) -> list:
        """Returns the leaderboard from the database."""
        result = self.leaderboard_collection.aggregate([
            {"$match": {"score": {"$gt": 0}}},
            {"$sort": {"score": -1}}
        ])
        return list(result)

    def get_user_score(self, username: str) -> int:
        """Returns the user's score from the leaderboard."""
        result = self.leaderboard_collection.find_one({"username": username})
        return result

    def add_user_to_leaderboard(self, username: str, avatar: str) -> None:
        """Adds a user to the leaderboard."""
        self.leaderboard_collection.insert_one({"username": username, "score": 0, "avatar": avatar})

    def update_leaderboard(self, username: str, score: int) -> None:
        """Updates the leaderboard with username and score"""
        self.leaderboard_collection.update_one(
            {"username": username},
            {"$set": {"score": score}},
            upsert=True
        )
    
    #Games
    def create_game(self, game_data) -> str:
        """Creates a new game and returns the game ID."""
        game_id = self.games_collection.insert_one(game_data).inserted_id
        return str(game_id)

    def get_game(self, game_id) -> dict:
        """Retrieves a game document from the database."""
        game_data = self.games_collection.find_one({"_id": ObjectId(game_id)})
        return game_data

    def update_game(self, game_id, game_data) -> None: 
        """Updates a game document in the database."""
        self.games_collection.update_one({"_id": ObjectId(game_id)}, {"$set": game_data})

    #Random word generator
    def get_words_count(self) -> int:
        """Returns the number of words in the database."""
        return self.words_collection.count_documents({})

    def get_random_word_page(self) -> int:
        """Returns a random word from the database."""
        random_document = self.words_collection.aggregate([
            {"$sample": {"size": 1}}
        ])
        return random_document.next() if random_document else None

    def delete_word(self, word: str) -> None:
        """Deletes a word from the database."""
        self.words_collection.delete_one({"word": word})

    def update_page(self, word: str, page: int) -> None:
        """Updates the page of a word in the database."""
        self.words_collection.update_one(
            {"word": word},
            {"$set": {"page": page}}
        )
