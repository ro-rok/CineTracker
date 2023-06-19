# Movie Website - Explore and Discover Movies

This project is a web application that allows users to explore and discover movies. It provides functionalities such as searching for movies, viewing movie details, registering as a user, and logging in/out. The application uses the OMDb API to fetch movie data and MongoDB for data storage.

## Project Structure

The project structure is as follows:

- [`main.py`](https://github.com/ro-rok/Movie_OMDB/blob/main/app/main.py): The main Python file that contains the FastAPI application.
- [`database.py`](https://github.com/ro-rok/Movie_OMDB/blob/main/app/database.py): A Python file that handles the database operations using MongoDB.
- [`static/`](https://github.com/ro-rok/Movie_OMDB/tree/main/static): A directory that contains static files such as CSS and JavaScript files.
- [`templates/`](https://github.com/ro-rok/Movie_OMDB/tree/main/templates): A directory that contains HTML templates for rendering the web pages.

## Features

The Movie Website includes the following features:

### Homepage:
-Carousel for Movie Posters: The homepage features a carousel that displays movie posters. Users can navigate through the carousel to view different movie posters.<br />
-Movie Details: Clicking on a movie poster in the carousel will reveal the user to the movie details page. The movie details page provides compendious information about the selected movie, including its title, cast, plot, director, release date, and IMDb rating.<br />
-Synopsis Display: By double-clicking on a movie poster, users can switch between viewing the detailed movie information and a brief synopsis.<br />
-Sidebar: The sidebar changes based on whether the user is logged in or not. When logged in, it displays user details, including the user's avatar and username.<br />
-Search Form: The website provides a search form that allows users to search for movies based on their query. The search results page displays a list of movies related to the search query.<br />

### Movie Details
-Movie Details Page:<br />
• The /movie/{imdb_id} route renders the movie.html template for the specified IMDb ID.<br />
• It retrieves movie data from the MongoDB database and, if not found, creates a new movie entry using the IMDb ID.<br />
• The movie details page displays information such as title, year, genre, director, actors, plot, and poster image.<br />

### Movie Search
-Movie Search Functionality:<br />
• The /search route allows users to search for movies based on a query string.<br />
• It retrieves search results from the OMDb API using the provided query and displays the results in the search.html template.<br />
• The search results include movie titles, release years, and posters.<br />


### User Registration
-User Registration Page:<br />
• The /register route renders the register.html template, which displays a registration form.<br />
• Users can enter a username, password, confirm password, and choose an avatar image.<br />
• The registration form validates the input and adds a new user to the MongoDB database if all requirements are met.<br />

### User Login/Logout
-User Login Page: <br />
• The /login route renders the login.html template, which displays a login form.<br />
• Users can enter their username and password to log into the application.<br />
• The login form verifies the user's credentials and sets the user ID in a cookie upon <br />

-User Logout: <br />
• The /logout route logs out the user by deleting the user ID cookie.<br />
• After logging out, the user is redirected to the homepage.<br />


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
