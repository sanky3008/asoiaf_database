from unittest import result
from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
import os
import requests
import sqlite3
import connector
from ast import literal_eval
import fetcher

app = Flask(__name__)

books_url = ""
character_url = ""
houses_url = ""

@app.route('/', methods = ["GET"])
def index():
    fetcher.update_all()
    return render_template('homepage.html')

@app.route('/books', methods = ["GET", "POST"])
def getbooks():
    #Fetch book list from DB and give it to the books.html file
    if request.method == "GET":
        books = connector.fetch_books()
        return render_template("book_list.html", books = books)
    return render_template('homepage.html')

@app.route('/bookdetails', methods = ["GET"])
def getbookdetails():
    #Fetch book details from DB and give it to bookdetails.html file
    book_url = request.args.get("url")
    bookdetails = connector.getbookdetails(book_url)
    return render_template("bookdetails.html", details = (bookdetails, literal_eval(bookdetails["authors"])))

@app.route('/characters', methods = ["GET", "POST"])
def getcharacters():
    #Fetch character list from DB and give it to the book_list.html
    if request.method == "GET":
        characters = connector.fetch_characters()
        return render_template("character_list.html", characters = characters)
    return render_template("homepage.html")

@app.route('/characterdetails', methods = ["GET"])
def getchardetails():
    #Fetch book details from DB and give it to bookdetails.html file
    char_url = request.args.get("url")
    chardetails = connector.getchardetails(char_url)
    return render_template("characterdetails.html", details = (chardetails, literal_eval(chardetails["aliases"]), literal_eval(chardetails["tvSeries"])))

@app.route('/houses', methods = ["GET", "POST"])
def gethouses():
    #Fetch house list from DB and give it to house_list.html
    if request.method == "GET":
        houses = connector.fetch_houses()
        return render_template("house_list.html", houses = houses)
    return render_template("homepage.html")

@app.route('/housedetails', methods = ["GET"])
def gethousedetails():
    #Fetch book details from DB and give it to bookdetails.html file
    house_url = request.args.get("url")
    housedetails = connector.gethousedetails(house_url)
    return render_template("housedetails.html", details = (housedetails, literal_eval(housedetails["titles"]), literal_eval(housedetails["seats"])))

@app.route('/search', methods = ["GET", "POST"])
def search():
    #Render search.html
    if request.method == "GET":
        return render_template("search.html")
    elif request.method == "POST":
        string = request.form.get("string")
        results = connector.search(string)
        return jsonify({'results': results})
    return render_template("homepage.html")

if __name__ == '__main__':
    app.run(debug = True)
