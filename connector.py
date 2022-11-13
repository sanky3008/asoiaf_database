from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
import os
import requests
import sqlite3
import fetcher
from ast import literal_eval
import json

def fetch_books():
    con = sqlite3.connect("got.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    con.close()
    return rows

def getbookdetails(url):
    con = sqlite3.connect("got.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM books WHERE url = ?", (url,))
    rows = cur.fetchone()
    con.close()
    return rows

def fetch_characters():
    con = sqlite3.connect("got.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM characters")
    rows = cur.fetchall()
    con.close()
    return rows

def getchardetails(url):
    con = sqlite3.connect("got.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM characters WHERE url = ?", (url,))
    rows = cur.fetchone()
    con.close()
    return rows

def fetch_houses():
    con = sqlite3.connect("got.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM houses")
    rows = cur.fetchall()
    con.close()
    return rows

def gethousedetails(url):
    con = sqlite3.connect("got.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM houses WHERE url = ?", (url,))
    rows = cur.fetchone()
    con.close()
    return rows

def search(string):

    if not string:
        return []
    else:
        con = sqlite3.connect("got.db")
        #con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        #search booksearch
        cur.execute('SELECT * FROM booksearch WHERE booksearch MATCH ?', (string,))
        bookresults = cur.fetchall()

        #search charsearch
        cur.execute("SELECT * FROM charsearch WHERE charsearch MATCH ?", (string,))
        charresults = cur.fetchall()

        #search housesearch
        cur.execute("SELECT * FROM housesearch WHERE housesearch MATCH ?", (string,))
        houseresults = cur.fetchall()

        con.close()

        results = []
        for book in bookresults:
            results.append(json.dumps({"type": "book", "name": book[1], "url": book[0]}))
        
        for char in charresults:
            results.append(json.dumps({"type": "character", "name": char[1], "url": char[0]}))
        
        for house in houseresults:
            results.append(json.dumps({"type": "house", "name": house[1], "url": house[0]}))

        return results

#print(search("A"))