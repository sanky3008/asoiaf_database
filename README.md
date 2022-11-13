# ASOIAF DATABASE
## Video Demo:  <URL https://youtu.be/gFC71OlhLKE>
## Description:
Hello I am Sankalp Phadnis from India and ASOIAF Database is my CS50 final project. This database uses [An API of Ice and Fire](https://anapioficeandfire.com/) to get data of the ASOIAF universe in a searchable and presentable format.

There are mainly 3 modules of this project, which bring together this app. They are:
- Fetcher
- Main App
- Search

### Fetcher:
The [fetcher](/fetcher.py) connects to the external API used in this project, and stores its data in the database [got.db](/got.db). To facilitate this, it uses the python requests library, to connect to An API of Ice and Fire and get details on books, characters and houses via the 3 APIs they have provided. 

#### Choice of database and schema:
The data for books, characters & houses also contained arrays, which needed to be stored in the database for the app to access. To enable this, there were 3 choices:
- Make multiple tables to store each variable's mapping by decontructing the array -> This choice was eliminated as it would have required 16 tables, which wasn't justifiable due to low scale of the data and limited use-cases.
- Use MySQL to store JSONs directly -> This choice was eliminated as MySQL requires the database to be stored on a server, and the cost + complexity did not justify the scale.
- Convert the array into a string using repr() and then reconvert it to the array using literal_eval() -> This was chosen as it was less complex, and it was only converting strings which were made using repr() so there was no risk.

You can find the database schema [here](https://emphasized-bird-905.notion.site/ASOIAF-Database-270186b6ebac4302bf2a9823b4ca414f).

The fetcher was made seperate so as to limit the number of API calls to the server, as the nature of the data is static (it won't change at a high frequency). Although for now the database is updated everytime the '/' URL is called, this can be changed into a daily cronjob when the website is hosted on a linux server rather than locally on computer.

### Main App:
Main App gives all of the functionalities of the app to the user. For querying the database, it uses [connector.py](/connector.py) and its methods.

The [main app](/app.py) allows the user to access the following:
1. [Homepage](/templates/homepage.html) - Entry points to book list, character list, house list and search
2. [Book List](/templates/book_list.html) - [app.py](/app.py) fetches list of books via methods in [connector.py](/connector.py) and shows them in the frontend.
3. [Book Details](/templates/bookdetails.html) - [app.py](/app.py) uses the methods in [connector.py](/connector.py) to fetch details of each of the selected book and shows it in the frontend.
4. [Character List](/templates/character_list.html) - [app.py](/app.py) fetches list of characters via methods in [connector.py](/connector.py) and shows them in the frontend.
5. [Character Details](/templates/characterdetails.html) - [app.py](/app.py) uses the methods in [connector.py](/connector.py) to fetch details of each of the selected character and shows it in the frontend.
6. [House List](/templates/house_list.html) - [app.py](/app.py) fetches list of houses via methods in [connector.py](/connector.py) and shows them in the frontend.
7. [House Details](/templates/housedetails.html) - [app.py](/app.py) uses the methods in [connector.py](/connector.py) to fetch details of each of the selected house and shows it in the frontend.

### Search:
The search module searches across the database to provide suggestions & results. In order to do that, it uses the FTS5 (Full text search 5) extension of Sqlite3. Through this extension, virtual tables were created for books, characters and houses that involved columns/variables that are searchable. The schema of the same is included in the notion link of data schema.

Whenever the user types a letter (on keydown event), the particular string at that point of time is used to query across all 3 virtual tables, find matching results and combine them in one list at frontend. To connect the frontend to the database, there were 2 options:
1. Query the data directly using Javascript -> this was eliminated as not all browsers support this
2. POST request to /search at every keydown -> this was used in the search. At every keydown event, the string is sent via POST request to /search in [app.py](/app.py). It then fetches the result by querying the virtual tables through [connector.py](/connector.py). The results are then sent back as the response of the POST request, which is then reflected on frontend. For this asynchronus communication between backend and frontend, jQuery AJAX are used.

