########################
# flask app
########################
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape
###################################
# data base set up
###################################
# Flask set up
app = Flask(__name__)
# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html",data = data )

###################################
# data scraping
###################################
@app.route("/scrape")
def scrape():
    #run the scrape function
    mars_data= scrape.scrape()

    mongo.db.collection.update({},mars_data, upsert=True)
    #return to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)