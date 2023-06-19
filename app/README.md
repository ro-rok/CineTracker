# Code Overview for main.py

```python
async def omdb_search(word: str, page: int) -> tuple:
   # Fetches movies from the OMDb API based on the provided search term 'word' and page number 'page'
   # Returns a tuple with a boolean value indicating the success of the API request and the list of movies retrieved 
```
   
```python
async def get_current_user_id(request: Request) -> str:
   # Retrieves the current user ID from the cookies stored in the 'request'
   # Returns the user ID as a string '''
   ```
   
```python 
async def fetch_random_movies(value=-1, word_list=word_list):
   # Fetches 20 random movies from the OMDb API and stores them in the MongoDB database
   # If 'value' is provided, the corresponding word is removed from the 'word_list' to avoid repetition 
   ```
   
```python 
async def read_root(request: Request, current_user_id: str = Depends(get_current_user_id)):
   # Handles the root route ("/") and renders the 'index.html' template
   # Calls the 'fetch_random_movies' function to retrieve random movies
   # Retrieves the 15 most recently released movies from the MongoDB database
   # If a user is logged in, retrieves the user information based on the 'current_user_id' 
   ```
   
```python
async def movie_page(imdb_id: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
   # Handles the route for movie pages ("/movie/{imdb_id}") and renders the 'movie.html' template for the specified IMDb ID
   # Retrieves movie data from the MongoDB database based on the 'imdb_id'
   # If the movie data is not found, creates a new movie entry using the IMDb ID
   # If a user is logged in, retrieves the user information based on the 'current_user_id'
   ```
   
```python
async def search_movies(query: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
   # Handles the movie search route ("/search") and renders the 'search.html' template
   # Searches for movies based on the provided 'query' by making requests to the OMDb API
   # Retrieves search results and displays them in the template
   # If a user is logged in, retrieves the user information based on the 'current_user_id' 
   ```
   
```python
async def register(request: Request):
   # Handles the user registration route ("/register") and renders the 'register.html' template
   # Displays the registration form where users can enter their username, password, confirm password, and choose an avatar image 
   ```
   
```python
async def process_registration(request: Request):
   # Processes the registration form submitted by the user
   # Validates the form input, including password matching and username availability
   # Adds a new user to the MongoDB database with the provided information
   # Sets the user ID in a cookie and redirects the user to the homepage ("/") 
   ```
   
```python
async def login(request: Request):
   # Handles the user login route ("/login") and renders the 'login.html' template
   # Displays the login form where users can enter their username and password
   ```
   
```python
async def process_login(request: Request, username: str = Form(...), password: str = Form(...)):
   # Processes the login form submitted by the user
   # Verifies the user's credentials and sets the user ID in a cookie upon successful login
   # Redirects the user to the homepage ("/") if the login is successful or displays an error message if the login fails 
   ```
   
```python
async def logout(request: Request):
   # Handles the user logout route ("/logout") and logs out the user
   # Deletes the user ID cookie and redirects the user to the homepage ("/") 
   ```
