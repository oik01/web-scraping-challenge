from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.Mars_db
# Create empty Collection
Mars = db.Mars
# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Run the scrape function
    #Content = scrape_mars.scrape()

    # Add to mongo database
    #db.Mars.update({}, Content, upsert=True)
    # Find one record of data from the mongo database
    Content = db.Mars.find_one()
    # Return template and data
    return render_template("index.html", Content= Content, data = Content['html_table'])


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    Content = scrape_mars.scrape()

    # Add to mongo database
    db.Mars.update({}, Content, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
