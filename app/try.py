import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import random
import httpx
from typing import List
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.DEBUG)


@app.get("/")
async def read_root(request: Request):
    movies = [{
"Title": "Spider-Man: No Way Home",
"Year": "2021",
"Rated": "PG-13,Released:  datetime(2022, 1, 14, 0, 0)",
"Runtime": "148 min",
"Genre": "Action, Adventure, Fantasy",
"Director": "Jon Watts",
"Writer": "Chris McKenna, Erik Sommers, Stan Lee",
"Actors": "Tom Holland, Zendaya, Benedict Cumberbatch",
"Plot": "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man.",
"Language": "English",
"Country": "United States",
"Awards": "Nominated for 1 Oscar. 35 wins & 69 nominations total",
"Poster": "https://m.media-amazon.com/images/M/MV5BZWMyYzFjYTYtNTRjYi00OGExLWE2YzgtOGRmYjAxZTU3NzBiXkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_SX300.jpg",
"Ratings": [
{
"Source": "Internet Movie Database",
"Value": "8.2/10"
},
{
"Source": "Rotten Tomatoes",
"Value": "93%"
},
{
"Source": "Metacritic",
"Value": "71/100"
}
],
"Metascore": "71",
"imdbRating": "8.2",
"imdbVotes": "798,343",
"imdbID": "tt10872600",
"Type": "movie",
"DVD": "N/A",
"BoxOffice": "$814,115,070",
"Production": "N/A",
"Website": "N/A",
"Response": "True"
},{"Title":"The Dark Knight","Year":"2008","Rated":"PG-13,Released: datetime(2022, 1, 14, 0, 0)","Runtime":"152 min","Genre":"Action, Crime, Drama",
"Director":"Christopher Nolan","Writer":"Jonathan Nolan, Christopher Nolan, David S. Goyer","Actors":"Christian Bale, Heath Ledger, Aaron Eckhart",
"Plot":"Set within a year after the events of Batman Begins (2005), Batman, Lieutenant James Gordon, and new District Attorney Harvey Dent successfully begin to round up the criminals that plague Gotham City, until a mysterious and sadistic criminal mastermind known only as \"The Joker\" appears in Gotham, creating a new wave of chaos. Batman's struggle against The Joker becomes deeply personal, forcing him to \"confront everything he believes\" and improve his technology to stop him. A love triangle develops between Bruce Wayne, Dent, and Rachel Dawes.",
"Language":"English, Mandarin","Country":"United States, United Kingdom",
"Awards":"Won 2 Oscars. 162 wins & 163 nominations total","Poster":"https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg",
"Ratings":[{"Source":"Internet Movie Database","Value":"9.0/10"},{"Source":"Rotten Tomatoes","Value":"94%"},{"Source":"Metacritic","Value":"84/100"}],
"Metascore":"84","imdbRating":"9.0","imdbVotes":"2,719,396","imdbID":"tt0468569","Type":"movie","DVD":"09 Dec 2008",
"BoxOffice":"$534,987,076","Production":"N/A","Website":"N/A","Response":"True"},{'Title': 'The Cutting Edge: The Magic of Movie Editing', 'Year': '2004', 'imdbID': 'tt0428441', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZDM2ZTE5Y2ItYjQwYi00Yzk2LThjZWUtYzI4YmVjNjkwNTc1L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg'}, 
                {'Title': 'Spanish Movie', 'Year': '2009', 'imdbID': 'tt1467391', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BOGQ2NDM2ZTYtOWM3MS00NTBhLWI4YjktNjc0ZWRlYjhiNjY1XkEyXkFqcGdeQXVyMTY5MDE5NA@@._V1_SX300.jpg'}, 
                {'Title': 'Killer Movie', 'Year': '2008', 'imdbID': 'tt0988083', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMzAxOTg0NTg5Ml5BMl5BanBnXkFtZTcwMTE3MTAyMg@@._V1_SX300.jpg'}, 
                {'Title': 'Horrible Histories: The Movie - Rotten Romans', 'Year': '2019', 'imdbID': 'tt7715070', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZTg2NzJiZTQtOTI5Mi00MjA4LWJmNWQtMjc5ZjZhYjRkMGRhXkEyXkFqcGdeQXVyNjM1MDIzMTc@._V1_SX300.jpg'}, 
                {'Title': 'Swearnet: The Movie', 'Year': '2014', 'imdbID': 'tt2380564', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMjM3MzU2NjM2OF5BMl5BanBnXkFtZTgwMTI2MzE1MjE@._V1_SX300.jpg'}, 
                {'Title': 'Rudolph the Red-Nosed Reindeer: The Movie', 'Year': '1998', 'imdbID': 'tt0137201', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZjQyMmQ0OTQtZTBjZC00OTNjLWFiNGEtOTQxNWIyOGVhMGVlXkEyXkFqcGdeQXVyNzY1NDgwNjQ@._V1_SX300.jpg'}, 
                {'Title': 'Horrid Henry: The Movie', 'Year': '2011', 'imdbID': 'tt1684555', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BYjM4MjNmNGMtZGQzYi00OWJmLWJlYmEtOTY2ZDdkNTJlOGY0XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_SX300.jpg'}, 
                {'Title': 'Bleach the Movie: Hell Verse', 'Year': '2010', 'imdbID': 'tt1785394', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZWI1MTkxMmQtNjgyZC00YjhhLTlhZGQtYzcwODg5MDkzMjYzXkEyXkFqcGdeQXVyMTA3OTEyODI1._V1_SX300.jpg'}, 
                {'Title': 'Gintama the Movie: The Final Chapter - Be Forever Yorozuya', 'Year': '2013', 'imdbID': 'tt2374144', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZDhmMTNkZjYtMjFhZi00OWY1LWEwMDAtNGYxMDk5ZjIxMjkyXkEyXkFqcGdeQXVyNjc3OTE4Nzk@._V1_SX300.jpg'}, 
                {'Title': 'Pokémon the Movie: The Power of Us', 'Year': '2018', 'imdbID': 'tt8108230', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BY2ViM2I4OTktNDRmOS00NmZlLThjYWQtZTBhY2JlNTU3YzdhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg'},
                {'Title': 'Total Frat Movie', 'Year': '2016', 'imdbID': 'tt3879074', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTk0MTk1MzcwMV5BMl5BanBnXkFtZTgwMjg4NTYyOTE@._V1_SX300.jpg'}, 
                {'Title': 'The Gong Show Movie', 'Year': '1980', 'imdbID': 'tt0080808', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BY2I1ZGNjYjUtZGRjOC00YTQ1LWE5ZDMtYTRmYzQ3YjE4MTBmXkEyXkFqcGdeQXVyODkxMTU1Njc@._V1_SX300.jpg'},
                {'Title': 'The Sex Movie', 'Year': '2006', 'imdbID': 'tt0823188', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTY1MjA4MDgzNF5BMl5BanBnXkFtZTcwOTA3MDU1MQ@@._V1_SX300.jpg'}, 
                {'Title': 'Rat Movie: Mystery of the Mayan Treasure', 'Year': '2014', 'imdbID': 'tt7454352', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZTA5MzVmYWMtYThkMC00ZDRhLTllN2YtOTgyYjUzOWYyNjQ3XkEyXkFqcGdeQXVyNTkwOTYxMTc@._V1_SX300.jpg'}, 
                {'Title': '24x36: A Movie About Movie Posters', 'Year': '2016', 'imdbID': 'tt5003654', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BNjAyOTk1NDUxNl5BMl5BanBnXkFtZTgwNjg4NzgwMDI@._V1_SX300.jpg'}, 
                {'Title': 'The Prince and the Pauper: The Movie', 'Year': '2007', 'imdbID': 'tt0874424', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BY2I0ODIxNzktNDE0Yi00N2U4LTg2NjQtNWUzOTc4MzBhNzI3L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMjYzMjA3NzI@._V1_SX300.jpg'}, 
                {'Title': 'Pudsey the Dog: The Movie', 'Year': '2014', 'imdbID': 'tt3171246', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BNzg2MjcwOTkwM15BMl5BanBnXkFtZTgwOTM3MTEyMjE@._V1_SX300.jpg'}, 
                {'Title': 'Flatland: The Movie', 'Year': '2007', 'imdbID': 'tt0814106', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTI4MjI4Mzc0Nl5BMl5BanBnXkFtZTcwNDA1Nzk0MQ@@._V1_SX300.jpg'}, 
                {'Title': 'Blinky Bill the Movie', 'Year': '2015', 'imdbID': 'tt3700456', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTg3NjI5OTUzMV5BMl5BanBnXkFtZTgwNjE3NDI3NjE@._V1_SX300.jpg'}, 
                {'Title': 'Doraemon the Movie: Nobita and the Birth of Japan', 'Year': '2016', 'imdbID': 'tt5544700', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BNDk5NmFlMWYtNGY0NC00YTg4LTk0ODAtOTkzYzRlYzQyOTExXkEyXkFqcGdeQXVyNDQ1NDczMzU@._V1_SX300.jpg'},
                {'Title': 'Vidal Sassoon: The Movie', 'Year': '2010', 'imdbID': 'tt1649433', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTY3NTc2MTQzNF5BMl5BanBnXkFtZTcwNDk1MjIzNA@@._V1_SX300.jpg'}, 
                {'Title': 'How Not to Make a Movie', 'Year': '2013', 'imdbID': 'tt4053592', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZWJhNjVkMTMtN2Q5Yy00YWRlLWI2MjktZmVkMWRjYzFkYTJlXkEyXkFqcGdeQXVyMjIzMTk0MzM@._V1_SX300.jpg'}, 
                {'Title': 'Rat Movie 2: The Movie', 'Year': '2015', 'imdbID': 'tt7456044', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BYWJmMzY5NWQtMWRjZi00YjIyLWE2MjMtNTBjMTY1ZDA5YjhlXkEyXkFqcGdeQXVyNzk0ODcyNDQ@._V1_SX300.jpg'}, 
                {'Title': 'Trick the Movie: Psychic Battle Royale', 'Year': '2010', 'imdbID': 'tt1547631', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZmI3YTE5MzAtNDA1Zi00NjIzLWE3ZTQtYzMxMjlmMGI0ODljXkEyXkFqcGdeQXVyMjY0MDY4Mjk@._V1_SX300.jpg'}, 
                {'Title': 'Laid-Back Camp Movie', 'Year': '2022', 'imdbID': 'tt14364238', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMDQ1Y2U0MTktOTBmYS00N2I4LTg1MjktMmMxNTUzOTlhNGNjXkEyXkFqcGdeQXVyMzgxODM4NjM@._V1_SX300.jpg'}, 
                {'Title': 'Going Attractions: The Definitive Story of the Movie Palace', 'Year': '2019', 'imdbID': 'tt7248524', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BYWMzNmFkOTMtZjA1Yi00NTI0LWIxZTYtMTU4N2I3NGRiNzViXkEyXkFqcGdeQXVyNTY5OTU0NA@@._V1_SX300.jpg'}, 
                {'Title': 'Movie: Marrying the Mafia 3 - Family Hustle', 'Year': '2006', 'imdbID': 'tt0891485', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTgzMzEzMDM3Ml5BMl5BanBnXkFtZTgwMTE1MTA2MDE@._V1_SX300.jpg'}, 
                {'Title': 'SBK: The Movie', 'Year': '2014', 'imdbID': 'tt4227032', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTg3MzU4MDQ2MV5BMl5BanBnXkFtZTgwNTI5NjE2NDE@._V1_SX300.jpg'}, 
                {'Title': 'Midnight Movie Massacre', 'Year': '1988', 'imdbID': 'tt0095630', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMzdjMWFmMWYtNzVmYS00ZGVjLTg5MjQtZDI5Mjg4NGRhOWM1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'}, 
                {'Title': 'Giuseppe Makes a Movie', 'Year': '2014', 'imdbID': 'tt3661072', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMTc4NzE4MzYxM15BMl5BanBnXkFtZTgwNzM0NDMzMjE@._V1_SX300.jpg'}, 
                {'Title': "The Bob's Burgers Movie", 'Year': '2022', 'imdbID': 'tt7466442', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BYzFhNDNkY2UtYjc3ZS00NzVkLTlhNzEtYmZiZGMzYmRjMjVhXkEyXkFqcGdeQXVyMjQwMDg0Ng@@._V1_SX300.jpg'},
                {'Title': 'Ray Donovan: The Movie', 'Year': '2022', 'imdbID': 'tt14124268', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMThkMTBiMDItZGVhOC00MWJkLThlZjgtNmJiMTA0NjFjMDgyXkEyXkFqcGdeQXVyOTA3MTMyOTk@._V1_SX300.jpg'}, 
                {'Title': 'Rise of the Teenage Mutant Ninja Turtles: The Movie', 'Year': '2022', 'imdbID': 'tt9784708', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZmIxYmFlNjQtYmU0NC00MWMzLTkyYTktYTBjZmE5NDRlODEyXkEyXkFqcGdeQXVyMTEzMTI1Mjk3._V1_SX300.jpg'}, 
                {'Title': 'Monster High: The Movie', 'Year': '2022', 'imdbID': 'tt1447981', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BNTQyOTBhOTctZjk4MC00MGM3LTg0YTAtNDlhYjYyYWYxMGJiXkEyXkFqcGdeQXVyODUwNjEzMzg@._V1_SX300.jpg'}, 
                {'Title': 'The Nan Movie', 'Year': '2022', 'imdbID': 'tt10398318', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BNWNhMDI0ZmQtNjQ5Yi00ZWY4LWFkYzMtYzY0MWY3NzhlNDc3XkEyXkFqcGdeQXVyMTM1MjI0NTc2._V1_SX300.jpg'}, 
                {'Title': 'The Quintessential Quintuplets Movie', 'Year': '2022', 'imdbID': 'tt15721650', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZGZlOTcxZWItZDA3Yy00ZDNhLTllZjktMTVhZjQzZDkxNTYxXkEyXkFqcGdeQXVyMzgxODM4NjM@._V1_SX300.jpg'}, 
                {'Title': 'The Soccer Football Movie', 'Year': '2022', 'imdbID': 'tt22774688', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BNTliOGM3ODktNDIxMC00NWY3LTg5NTAtZTFkMzhkMGNjNmRhXkEyXkFqcGdeQXVyMTA5ODEyNTc5._V1_SX300.jpg'}, 
                {'Title': 'That Time I Got Reincarnated as a Slime the Movie: Scarlet Bond', 'Year': '2022', 'imdbID': 'tt15467380', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BOThmNDE2ZWEtMjczYi00NDBjLWFiNTctMTk3MGE3MzBiNWI0XkEyXkFqcGdeQXVyODMyNTM0MjM@._V1_SX300.jpg'},
                {'Title': 'Sword Art Online the Movie: Progressive - Scherzo of Deep Night', 'Year': '2022', 'imdbID': 'tt15830702', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BNzExZjlkODEtNTNiNC00OGE4LWI0YTEtNzVjODU5NzFjN2FjXkEyXkFqcGdeQXVyMTEwMjgyMzIz._V1_SX300.jpg'}, 
                {'Title': "Doraemon the Movie: Nobita's Little Star Wars 2021", 'Year': '2022', 'imdbID': 'tt13740078', 'Type': 'movie', 'Poster': 'https://m.media-amazon.com/images/M/MV5BZTIyODAyMDYtODAyYi00NzJhLTg1NzYtNzhhODhkNGMzZDVlXkEyXkFqcGdeQXVyMTM2MDY0OTYx._V1_SX300.jpg'}]
    return templates.TemplateResponse("index.html", {"request": request, "movies": movies})

# Route to fetch movie details from the OMDb API based on IMDb ID
@app.get("/movie/{imdb_id}")
async def movie_page(imdb_id: str, request: Request):    
    if imdb_id=="tt0468569":
        movie_data = {"Title":"The Dark Knight","Year":"2008","Rated":"PG-13","Released":"18 Jul 2008","Runtime":"152 min","Genre":"Action, Crime, Drama",
                    "Director":"Christopher Nolan","Writer":"Jonathan Nolan, Christopher Nolan, David S. Goyer","Actors":"Christian Bale, Heath Ledger, Aaron Eckhart",
                    "Plot":"Set within a year after the events of Batman Begins (2005), Batman, Lieutenant James Gordon, and new District Attorney Harvey Dent successfully begin to round up the criminals that plague Gotham City, until a mysterious and sadistic criminal mastermind known only as \"The Joker\" appears in Gotham, creating a new wave of chaos. Batman's struggle against The Joker becomes deeply personal, forcing him to \"confront everything he believes\" and improve his technology to stop him. A love triangle develops between Bruce Wayne, Dent, and Rachel Dawes.",
                    "Language":"English, Mandarin","Country":"United States, United Kingdom",
                    "Awards":"Won 2 Oscars. 162 wins & 163 nominations total","Poster":"https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg",
                    "Ratings":[{"Source":"Internet Movie Database","Value":"9.0/10"},{"Source":"Rotten Tomatoes","Value":"94%"},{"Source":"Metacritic","Value":"84/100"}],
                    "Metascore":"84","imdbRating":"9.0","imdbVotes":"2,719,396","imdbID":"tt0468569","Type":"movie","DVD":"09 Dec 2008",
                    "BoxOffice":"$534,987,076","Production":"N/A","Website":"N/A","Response":"True"}
    else:
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=1a8d2b0d&plot=full"  # Replace YOUR_API_KEY with your OMDb API key
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            movie_data = response.json()
            print(response)
            print(templates.TemplateResponse("movie.html", {"request": request, "movie": movie_data}))
    return templates.TemplateResponse("movie.html", {"request": request, "movie": movie_data})


@app.get("/search")
async def search_movies(query: str, request: Request):
    base_url = "http://www.omdbapi.com/"
    api_key = "1a8d2b0d"  # Replace with your actual API key

    params = {
        "apikey": api_key,
        "s": query,
        "type": "movie",
        "r": "json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        data = response.json()

    if "Search" in data:
        movies = data["Search"]
    else:
        movies = []

    return templates.TemplateResponse("search.html", {"request": request, "movies": movies})