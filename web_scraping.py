from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraper

# Setup Flask App
app = Flask(__name__)

mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    hemisphere_dict = scraper.scrape()
    mars.update(
        {}, 
        hemisphere_dict, 
        upsert=True
    )
    return 

if __name__ == "__main__":
    app.run(debug=True)