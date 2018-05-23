from flask import Flask, render_template, redirect
import pymongo
from pymongo import MongoClient
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db= client.mars_db
collection = db.website_data

@app.route("/")
def home():
    mars_data = collection.find_one()
    return render_template('index.html', dict = mars_data)

@app.route("/scrape")
def scrape():
    mars_scrape = scrape_mars.mars_scrape()
    collection.update({}, {"$set":mars_scrape}, upsert=True)

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)    
