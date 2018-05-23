from flask import Flask, render_template, redirect
import pymongo
from pymongo import MongoClient
from scrape_mars import mars_scrape

app = Flask(__name__)

conn = 'mongodb://localhost:5000'
client = pymongo.MongoClient(conn)

db= client.mars_db
collection = db.website_data

@app.route("/")
def home():
    mars_data = collection.find_one()
    return render_template('index.html', data = mars_data)

@app.route("/scrape")
def scrape():
    mars_scrape = mars_scrape()
    collection.update({"id":1}, {"$set":mars_scrape}, upser=True)

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)    
