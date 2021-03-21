########################
# flask app
########################
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape
import pymongo
###################################
# data base set up
###################################
# Flask set up
app = Flask(__name__)
# Use PyMongo to establish Mongo connection
#initializing Pymongo to work with MongoDBs
mongo = PyMongo(app,uri= "mongodb://localhost:27017/run_this_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html",mars_data = mars_data )

###################################
# data scraping
###################################
@app.route("/scrape")
def scrape():
    #run the scrape function
    mars_data= mars_scrape.scrape()

    mongo.db.mars.update({}, mars_data, upsert=True)
    #return to home page
    return render_template("index.html", mars_data = mars_data)


if __name__ == "__main__":
    app.run(debug=True)