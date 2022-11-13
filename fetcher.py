from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
import os
import requests
import sqlite3
import json

#Get the list of URLs by calling the base API
def update_all():
    #Establish connection to the database
    con = sqlite3.connect("got.db", check_same_thread=False)
    cur = con.cursor()

    base_url = "https://www.anapioficeandfire.com/api"
    urls = requests.get(base_url).json()
    update_books(con, cur, urls)
    update_characters(con, cur, urls)
    update_houses(con, cur, urls)

    con.close()

#Update the books data
def update_books(con, cur, urls):
    # try:
        books = requests.get(urls["books"]).json()
        for book in books:
            book_json = book
            data = cur.execute("SELECT * FROM books WHERE url = ?", (book["url"],)).fetchone()
            if data != None:
                continue
            else:
                cur.execute("INSERT INTO books (url, name, isbn, authors, numberOfPages, publiser, country, mediaType, released, characters, povCharacters) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                        (book_json["url"], book_json["name"], book_json["isbn"], repr(book_json["authors"]), book_json["numberOfPages"], book_json["publisher"], \
                        book_json["country"], book_json["mediaType"], book_json["released"], repr(book_json["characters"]), repr(book_json["povCharacters"])))
                con.commit()
                cur.execute("INSERT INTO booksearch(url, name, isbn, publisher) VALUES(?,?,?,?)", (book_json["url"], book_json["name"], book_json["isbn"], book_json["publisher"]))
                con.commit()
        return 0
    # except:
    #     print("Problem with updating books database")
    #     return 1

#Update the characters data
def update_characters(con, cur, urls):
    try:
        characters = requests.get(urls["characters"]).json()
        for char in characters:
            data = cur.execute("SELECT * FROM characters WHERE url = ?", (char["url"],)).fetchone()
            if data != None:
                continue
            else:
                cur.execute("INSERT INTO characters (url, name, gender, culture, born, died, titles, aliases, father, mother, spouse, allegiances, books, povBooks, tvSeries, playedBy) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                        (char["url"], char["name"], char["gender"], char["culture"], char["born"], char["died"], repr(char["titles"]), repr(char["aliases"]), char["father"], char["mother"], char["spouse"], repr(char["allegiances"]),\
                            repr(char["books"]), repr(char["povBooks"]), repr(char["tvSeries"]), repr(char["playedBy"])))
                con.commit()
        return 0
    except:
        print("Problem with updating characters database")
        return 1

#Update the houses data
def update_houses(con, cur, urls):
    try:
        houses = requests.get(urls["houses"]).json()
        for house in houses:
            data = cur.execute("SELECT * FROM houses WHERE url = ?", (house["url"],)).fetchone()
            if data != None:
                continue
            else:
                cur.execute("INSERT INTO houses (url, name, region, coatOfArms, words, titles, seats, currentLord, heir, overlord, founded, founder, diedOut, ancestralWeapons, cadetBranches, swornMembers) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                        (house["url"], house["name"], house["region"], house["coatOfArms"], house["words"], repr(house["titles"]), repr(house["seats"]), house["currentLord"], house["heir"], \
                            house["overlord"], house["founded"], house["founder"], house["diedOut"], repr(house["ancestralWeapons"]), repr(house["cadetBranches"]), repr(house["swornMembers"])))
                con.commit()
        return 0
    except:
        print("Problem with updating houses database")
        return 1

update_all()


