# Project 1

Web Programming with Python and JavaScript

NAME: Muskan Vaswan
NAME OF WEB APPLICATION: REVIEWER

'env' is a file that sets the environment variables for the project.

      REGISTRATION:
Users can register for the website, providing  a username, a password and its confirmation. The information is stored  in the users table of the database.
  Error messages: if the user fails to type either password or username.


      LOGIN:
Users, once registered, can log in to the website with their username and password.
  Error messages: if the user fails to provide either username or password, if the user doesn't exist, if the password is incorrect.


      LOGOUT:
Logged in users can log out of the site.


      IMPORT.PY:
A program that took the books from the books.csv file and imported them into the books table of the database. the file has alredady been executed.


      SEARCH:
Once a user has logged in, they can search for a book. Users can type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, the website displays a list of possible matching results. If the user typed in only part of a title, ISBN, or author name, the search page finds matches for those as well!
  Error message: if no matches were found.


      BOOK PAGE:
When users click on a book from the results of the search page, they are taken to a book page, with details about the book: its title, author, ISBN number, and any reviews that users have left for the book on the website. Moreover, the average rating and the rating count from the goodreads API are also displayed.


      REVIEW SUBMISSION:
 On the book page, users can submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users cannot submit multiple reviews for the same book.


      API Access:
If users make a GET request to the website’s /api/<isbn> route, where <isbn> is an ISBN number, the website returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON follows the format:
            {
            "author": "Raymond E. Feist",
            "average_score": null,
            "isbn": "0380795272",
            "review_count": 0,
            "title": "Krondor: The Betrayal",
            "year": 1998
            }
