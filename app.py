from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps
import json
import urllib.parse

app = Flask(__name__) 

# Connection à la base de donnée distante
app.config['MONGO_URI'] = "mongodb+srv://admin:admin@ynovbdd.ayg81.mongodb.net/PhotosBDD"

mongo = PyMongo(app)

if __name__ == "__main__":
    app.run(debug=False)

@app.route("/")
def goToHome():
    return redirect('/photos')

# Page d'accueil et de recherche des photos
@app.route("/photos", methods=["GET", "POST"])
def home():
    matchList = {}
    varMatch = {}
    # Vérification si un requête est présente de l'url
    if request.args:
        # Vérification si des paramètres particuliers sont présents
        if request.args.get('nom'):
            nom = request.args.get('nom')
            nom.replace('+', ' ')
            matchList['nom']={'$regex':nom}

        if request.args.get('tags'):
            tags = request.args.get('tags')
            matchList['tags']={"$regex": tags}

        varMatch['$match']=matchList
        varProject = { "$project": { "_id": 1, "nom": 1, "tags": 1, "chemin": 1}}
        # Création de l'aggregation avec la BDD NoSQL
        items = mongo.db.Photos.aggregate([varMatch, varProject])
        resp = dumps(items)
        jsonData = json.loads(resp)
        return render_template('pages/page.html', jsonData = jsonData)

    # Affichage de la page si aucunze requête est éffectuée
    if request.method == 'GET':
        message = "Aucune photo recherchée"
        return render_template('pages/page.html', message=message)

# Page de login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('pages/login.html')
    if "submit" in request.form:
        return redirect('/photos')

# Page de l'information d'une image
@app.route("/info", methods=['GET', 'POST'])
def info():
    chemin = request.args.get('chemin')
    varMatch = { "$match": { "chemin": chemin}}
    items = mongo.db.Photos.aggregate([varMatch])
    resp = dumps(items)
    jsonData = json.loads(resp)

    return render_template('pages/info.html', jsonData = jsonData)

# Page pour upload une image
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    return render_template('pages/upload.html',)