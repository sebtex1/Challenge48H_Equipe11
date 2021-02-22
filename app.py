from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps
import json
import urllib.parse

app = Flask(__name__) 

app.config['MONGO_URI'] = "mongodb+srv://admin:admin@ynovbdd.ayg81.mongodb.net/PhotosBDD"

mongo = PyMongo(app)

if __name__ == "__main__":
    app.run(debug=False)

@app.route("/photos", methods=["GET", "POST"])
def home():
    matchList = {}
    varMatch = {}
    if request.args:
        if request.args.get('nom'):
            nom = request.args.get('nom')
            matchList['nom']={'$regex':nom}

        if request.args.get('tags'):
            tags = request.args.get('tags')
            matchList['tags']={"$and": [{"tags": tags}]}

        varMatch['$match']=matchList
        items = mongo.db.Photos.aggregate([varMatch])
        resp = dumps(items)
        jsonData = json.loads(resp)
        return render_template('pages/page.html', jsonData = jsonData)

    if request.method == 'GET':
        message = "Executez donc une recherche de photos"
        return render_template('pages/page.html', message=message)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('pages/login.html')
    if "submit" in request.form:
        return redirect('/photos')

