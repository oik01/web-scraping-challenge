from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.Mars_test
db.testcollection.insert_many([{'random': 'random1'}, {'random2':'random3'}])
results = db.testcollection.find() 
for result in results:
    print(result)