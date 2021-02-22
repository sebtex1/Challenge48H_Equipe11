from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps
import json

app = Flask(__name__) 

app.config['MONGO_URI'] = "mongodb+srv://admin:admin@ynovbdd.ayg81.mongodb.net/PhotosBDD"

mongo = PyMongo(app)

if __name__ == "__main__":
    app.run(debug=False)

@app.route("/") 
def home(): 
    varMatch = { "$match": {"$and": [{"tags": "Produit"}]} }
    varProject = { "$project": {"nom": 1, "chemin": 1, "tags": 1, "_id": 0}}
    # varSort = {}
    items = mongo.db.Photos.aggregate([varProject])
    resp = dumps(items)
    jsonData = json.loads(resp)
    return render_template('pages/page.html', jsonData = jsonData)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('pages/login.html')
    if "submit" in request.form:
        return redirect('/')

