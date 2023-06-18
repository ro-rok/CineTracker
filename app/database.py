import pymongo
import requests
from datetime import datetime
from passlib.hash import bcrypt
from bson import ObjectId



class MongoDB:
    def __init__(self, url: str):
        self.client = pymongo.MongoClient(url)
        self.db = self.client["movie_app"]
        self.movies_collection = self.db["movies"]
        self.users_collection = self.db["users"]
        self.reviews_collection = self.db["reviews"]

    def create_movie(self, imdb_id: str, random =False):
        if self.movies_collection.count_documents({"imdbID": imdb_id}) > 0:
            return  # Skip adding duplicate movies

        url1 = f"http://www.omdbapi.com/?i={imdb_id}&apikey=1a8d2b0d&plot=full"
        url2 = f"http://www.omdbapi.com/?i={imdb_id}&apikey=1a8d2b0d"

        int(str.split("93 min", " ")[0])
        
        response1 = requests.get(url1).json()
        temp = response1

        # Conditon checker 
        if random:
            if temp["Poster"]=="N/A" or int(str.split(temp["Runtime"]," ")[0])<60 or temp["imdbRating"] == "N/A" or temp["Director"]=="N/A":
                return

        # Fetch data from URL 1
        temp["Plot_l"] = temp.pop("Plot")
        temp["Released"] = datetime.strptime(temp.pop("Released"), "%d %b %Y")
        temp["Year"] = int(temp.pop("Year"))
        temp["imdbRating"] = float(temp.pop("imdbRating"))

        # Fetch data from URL 2
        response2 = requests.get(url2).json()
        temp["Plot_s"] = response2["Plot"]

        # Store the movie data in the database
        self.movies_collection.insert_one(temp)

    def retrieve_movie_details(self, imdb_id: str):
        return self.movies_collection.find_one({"imdbID": imdb_id})

    def update_movie_review(self, imdb_id: str, user_id: str, review: str):
        self.reviews_collection.update_one(
            {"imdbID": imdb_id, "user_id": user_id},
            {"$set": {"review": review}},
            upsert=True
        )

    def delete_movie_review(self, imdb_id: str, user_id: str):
        self.reviews_collection.delete_one({"imdbID": imdb_id, "user_id": user_id})

    def add_user(self, username: str, password: str, avatar: str):
        hashed_password = bcrypt.hash(password)
        user_id = str(self.users_collection.insert_one({"username": username, "hashed_password": hashed_password, "avatar": avatar}).inserted_id)
        return user_id
    
    def get_user_by_username(self, username: str):
        return self.users_collection.find_one({"username": username})
    
    def get_user_by_id(self, user_id: str):
        return self.users_collection.find_one({"_id": ObjectId(user_id)})


class Mongo_Admin:
    def __init__(self, url: str):
        self.client = pymongo.MongoClient(url)
        self.db = self.client["movie_app"]
        self.movies_collection = self.db["movies"]
        self.users_collection = self.db["users"]
        self.reviews_collection = self.db["reviews"]

    def delete_duplicates_movies(self):
        pipeline = [{"$group": {"_id": "$imdbID","count": {"$sum": 1},"duplicates": {"$addToSet": "$_id"}}},
                    {"$match": {"count": {"$gt": 1}}}]

        duplicate_docs = self.movies_collection.aggregate(pipeline)
        for doc in duplicate_docs:
            duplicate_ids = doc["duplicates"]
            # Keep the first document and delete the rest
            del_ids = duplicate_ids[1:]
            self.movies_collection.delete_many({"_id": {"$in": del_ids}})

    def fix_movie_schema(self):
        movies = self.movies_collection.find()

        for movie in movies:
            # Convert "Released" field to Date format
            released = movie.get("Released")
            if released:
                released_date = datetime.strptime(released, "%d %b %Y")
                self.movies_collection.update_one(
                    {"_id": movie["_id"]},
                    {"$set": {"Released": released_date}}
                )

            # Convert "Year" field to int
            year = movie.get("Year")
            if year:
                year_int = int(year)
                self.movies_collection.update_one(
                    {"_id": movie["_id"]},
                    {"$set": {"Year": year_int}}
                )
            
            rating=movie.get("imdbRating")
            if rating:
                rating_float= float(rating)
                self.movies_collection.update_one(
                    {"_id": movie["_id"]},
                    {"$set":{"imdbRating": rating_float}}
                )
    
    def delete_movieset(self, field: str, comparator: str):
        query = {field: comparator}
        self.movies_collection.delete_many(query)





