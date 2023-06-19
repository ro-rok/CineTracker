# Movie Website - Explore and Discover Movies

This project is a Movie Website that allows users to explore and discover movies. It provides features such as searching for movies, displaying movie details, and storing user preferences.

## Project Overview

The Movie Website is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+.

## Project Structure

The project structure is as follows:

- `main.py`: The main Python file that contains the FastAPI application.
- `static/`: A directory that contains static files such as CSS and JavaScript files.
- `templates/`: A directory that contains HTML templates for rendering the web pages.
- `database.py`: A Python file that handles the database operations using MongoDB.
- `README.md`: This file, providing an overview and documentation for the project.

## Features

The Movie Website includes the following features:

- User Authentication: Users can create an account and log in to the website.
- Movie Search: Users can search for movies based on various criteria.
- Movie Details: Detailed information about each movie is displayed, including title, release year, genre, and more.
- User Preferences: Users can save movies to their favorites or watchlist.
- Random Movie Suggestions: The website suggests random movies to users based on predefined word lists.
- API Integration: The OMDb API is used to fetch movie data.

## Getting Started

To run the Movie Website project, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/movie-website.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Set up a MongoDB database and update the connection string in `main.py` and `database.py`.
4. Run the application: `python main.py`
5. Open a web browser and navigate to `http://localhost:8000` to access the Movie Website.

## Dependencies

The project depends on the following Python libraries:

- `fastapi`: A web framework for building APIs.
- `httpx`: A fully featured HTTP client library.
- `passlib`: A password hashing library.
- `pymongo`: A MongoDB driver for Python.

## Contributing

Contributions to the Movie Website project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the project's GitHub repository.
