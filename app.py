from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True) # Now that we've gathered new data, we need to update the database 
   return redirect('/', code=302) # This will navigate our page back to / where we can see the updated content.


if __name__ == "__main__":
       app.run()
