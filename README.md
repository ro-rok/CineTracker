# CineTracker - Unleash your Inner Movie Buff

CineTracker is a web-based application designed for movie enthusiasts to explore, track, and review movies. It provides a user-friendly interface where users can discover new movies, add them to their personal lists, rate and review movies, and engage in a movie comparison game. The application leverages Python and HTML to create a seamless and interactive movie experience.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Features](#features)
    1. [Sidebar](#sidebar)
    2. [Search Form](#search-form)
    3. [Home Page](#home-page)
    4. [Movie Page](#movie-page)
    5. [Review Submission](#review-submission)
    6. [Search Page](#search-page)
    7. [Random Page](#random-page)
    8. [Movie List Page](#movie-list-page)
    9. [Registration](#registration)
    10. [Login Page](#login-page)
    11. [Logout](#logout)
3. [Movie Comparison Game](#movie-comparison-game)
    1. [How to Play](#how-to-play)
    2. [Game Introduction](#game-introduction)
    3. [Start Game](#start-game)
    4. [Game Page](#game-page)
    5. [Game Result](#game-result)
    6. [Game Over](#game-over)
4. [Getting Started](#getting-started)
5. [Dependencies](#dependencies)
6. [Contributing](#contributing)

## Project Structure

The project structure is as follows:

- [`main.py`](https://github.com/ro-rok/Movie_OMDB/blob/main/app/main.py): The main Python file that contains the FastAPI application.
- [`database.py`](https://github.com/ro-rok/Movie_OMDB/blob/main/app/database.py): A Python file that handles the database operations using MongoDB.
- [`static/`](https://github.com/ro-rok/Movie_OMDB/tree/main/static): A directory that contains static files such as CSS and JavaScript files.
- [`templates/`](https://github.com/ro-rok/Movie_OMDB/tree/main/templates): A directory that contains HTML templates for rendering the web pages.

## Features

### Sidebar

The sidebar is a fixed panel located on the left side of the website. It provides quick access to various sections and options based on the user's authentication status. It is almost ubiquitous to all HTML templates.

#### - Logo and Social Links

The sidebar includes the project logo and social media links for further engagement.

#### - Home Button

Clicking on the "Home" button in the sidebar will navigate users back to the home page.

#### - Random Button

The "Random" button allows users to explore random movies and discover new titles.

#### - User Details

If a user is logged in, the sidebar displays the user's avatar and username. The user can access their movie list, play the game, and log out using the corresponding buttons.

#### - Login Button

If a user is not logged in, the sidebar provides a "Login" button to allow users to authenticate and access additional features.

------------------

### Search Form

The search form enables users to search for specific movies using keywords. Users can enter their desired movie titles or keywords in the search input field. Upon submitting the search query, the website will display a list of movies related to the search term.

------------------

### Home Page

The home page serves as the main landing page for the Movie Website. It showcases several sections to engage users and provide movie recommendations.

#### - Movie Carousel

The home page features a carousel that displays movie posters. Users can swipe through the carousel to explore different movies.

#### - Click for More Info

Clicking on a movie poster in the carousel will take users to the movie details page, where they can find more information about the movie.

#### - Double-Click for Synopsis

If users double-click on a movie poster in the carousel, a small synopsis of the movie will be displayed instead of the full movie details.

#### - User Movies Section

If a user is logged in, the website displays a dedicated section for their movies. The section showcases movies that the user has added to their personal movie list. Users can click on a movie poster to view detailed information about the movie, including its cast, release date, director, and IMDb rating.

#### - Latest Movies Section

The latest movies section displays a selection of recently released movies. Users can explore these movies by swiping through the carousel. Clicking on a movie poster in this section will provide users with comprehensive details about the movie.

#### - Random Movies Section

The random movies section presents a collection of randomly selected movies. Users can discover and explore movies by swiping through the carousel. Clicking on a movie poster will direct users to the movie details page.

#### - Current Ranking Sidebar

The right sidebar shows the current ranking of users based on their scores. The top three users with the highest scores are displayed. Each user's rank, username, avatar, and score are visible.

------------------

### Movie Page

The movie page allows users to view detailed information about a specific movie. Users can see the movie's title, release date, genre, cast, director, writer, awards, box office, ratings, and plot. The movie details are fetched from a database and dynamically rendered on the movie page. The movie poster image is displayed alongside the movie details.

#### - User Actions

Users can interact with the movie page through various actions:

##### Add Movie to List

Users can add movies to their personal list and specify the category (Watched, Plan to Watch, or Dropped) and rating for each movie.

##### Update Movie Status and Rating

Users can update the status (category) and rating of movies in their list.

##### Delete Movie from List

Users can delete movies from their list.

#### - User Reviews

Users can write reviews for movies and provide a rating (score) and recommendation. Users can view their own reviews on the movie page and edit them if desired. Users can also view the latest reviews written by other users for the same movie. Reviews are displayed in a structured format, including the user's avatar, username, rating, recommendation, and review text.

------------------

### Review Submission

Users can submit reviews for movies on the Movie Website.

#### - Submit Review Page

The website provides a dedicated page for submitting movie reviews. Users can access this page by clicking on the "Submit Review" button on the movie details page.

#### - Movie Information

The review page displays the title of the movie for which the user is submitting the review. This information is fetched from the database based on the IMDb ID.

#### - Movie Poster

The review page showcases the movie poster to provide visual context for the review.

#### - Edit Review

If the user has already submitted a review for the movie, the review page allows them to edit their existing review.

#### - Add Review

If the user has not yet submitted a review for the movie, the review page provides a form to add a new review. The form includes fields for the review's status (watched or dropped), rating, recommendation, and review text.

#### - Update and Delete

Users can update their existing review by modifying the form fields and clicking the "Update" button. They also have the option to delete their review by clicking the "Delete Review" button. These actions are performed on the server and reflected in the database.

------------------

### Search Page

The search page enables users to search for movies based on specific queries. Users can enter a search query in the provided input field. Upon submitting the search query, the website fetches movies from an API based on the query. The search results are displayed in the "Search Results" section. Each movie is represented as a clickable card containing the movie title and poster. Clicking on a movie card redirects users to the movie details page.

------------------

### Random Page

The random page displays a selection of random movies to users. The website fetches a list of random movies from the database. The random movies are displayed in the "Random Results" section. Each movie is represented as a clickable card containing the movie title and poster. Clicking on a movie card redirects users to the movie details page.

------------------

### Movie List Page

The movie list page allows users to view and manage their movie list. The movie list is displayed in a table format, with columns including the movie title, score, status, and actions (update and delete).

#### - Sorting the Movie List

Users can sort the movie list based on different criteria by selecting a filter option. The available filter options are:

- Default: The movies are displayed in the order they were added to the list.
- Title (Ascending): The movies are sorted in alphabetical order by title in ascending order.
- Title (Descending): The movies are sorted in alphabetical order by title in descending order.
- Rating (Ascending): The movies are sorted based on the user's rating in ascending order.
- Rating (Descending): The movies are sorted based on the user's rating in descending order.

#### - Filtering the Movie List by Category

Users can filter the movie list based on the category of movies. The available categories are:

- All movies: Displays all the movies in the list.
- Watched: Displays only the movies that have been watched.
- Plan to Watch: Displays only the movies that are planned to be watched.
- Dropped: Displays only the movies that have been dropped.

#### - Search Movies

Users can search for movies by entering a query in the search input field and clicking the search button. The search results are displayed in the movie list table, showing only the movies that match the search query.

#### - Update Movie Category

Users can update the category of a movie by selecting a new category from the dropdown menu in the "Status" column of the movie list table. The category options available are "Watched," "Plan to Watch," and "Dropped." When the category is updated, the movie list is automatically refreshed to reflect the changes.

#### - Update Movie Rating

Users can update the rating of a movie by selecting a new rating from the set of stars in the "Score" column of the movie list table. The rating options range from 1 to 10 stars. When the rating is updated, the movie list is automatically refreshed to reflect the changes.

------------------

### Registration

The registration feature allows users to create a new account on the Movie Website.

#### - Registration Page

Users can access the registration page by navigating to the `/register` route. The registration page displays a form where users can enter their desired username, password, and confirm password. Users can also select an avatar from a range of options provided using a swiper component. Upon submitting the registration form, the form data is sent to the server via a POST request to the `/register` route.

#### - Registration Processing

The server processes the form data and validates the inputs. If the form data is valid, a new user is added to the database with the provided username, password, and avatar. The user is then redirected to the home page (`/`) and a cookie is set to store the user's ID. If there are any errors in the form data, the user is redirected back to the registration page and error messages are displayed.

------------------

### Login Page

The login page allows users to log into the Movie Website using their credentials.

#### - Login Form

The login form includes the following fields:

- Username: Users need to enter their username.
- Password: Users need to enter their password.
- Remember me: Users can select this option to have their login session persist across browser sessions.

#### - Login Processing

When the login form is submitted, the form data is sent to the server for processing. The server retrieves the user from the database based on the provided username. If the user doesn't exist or the password is incorrect, an error message is displayed on the login page. If the user exists and the password is correct, a cookie containing the user ID is set, and the user is redirected to the home page.

------------------

### Logout

Users can log out from the Movie Website, which deletes the user ID cookie and ends their session. When the logout action is triggered, the server deletes the user ID cookie associated with the user's session. After successfully logging out, users are redirected to the home page.

------------------

## Movie Comparison Game

The Movie Comparison Game is a web-based application that tests users' knowledge of IMDb movie ratings. The game presents users with pairs of movies and asks them to choose the movie with the higher IMDb rating. The game continues until the user loses all three lives.

### How to Play

1. Start the game by visiting the game introduction page (`/game`).
2. Read the game rules and click on the "Start the Game" button.
3. On the game page, compare the two movies displayed and choose the movie you think has the higher IMDb rating.
4. After making your choice, the game will inform you if your choice was correct or wrong.
5. The score and remaining lives will be updated accordingly.
6. The game continues with new movie comparisons until you lose all three lives.
7. When the game is over, your score and rank will be displayed on the game over page.

------------------

### Game Introduction

The game starts with an introduction page where the user can familiarize themselves with the rules of the game.

### Start Game

The user can start a new game by clicking the "Ready Up!" button. This action redirects the user to the game page.

### Game Page

The game page presents the user with pairs of movies and asks them to choose the movie with the higher IMDb rating. The user's current score and remaining lives are displayed on the page.

### Game Result

After choosing a movie, the game evaluates the user's selection and displays a notification indicating whether the choice was correct or incorrect. The user's score is incremented for correct choices, and lives are deducted for incorrect choices.

### Game Over

When the user loses all three lives, the game is over. The user is redirected to the game over page, where their final score and rank on the leaderboard are displayed.

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
