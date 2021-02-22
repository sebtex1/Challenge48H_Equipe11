from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps
import json

app = Flask(__name__) 

app.config['MONGO_URI'] = "mongodb+srv://admin:admin@ynovbdd.ayg81.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route("/") 
def home(): 
    varMatch = {}
    varProject = {}
    varSort = {}
    all = mongo.db.Photos.aggregate([varMatch, varProject, varSort])
    resp = dumps(all)
    jsonData = json.loads(resp)
    return render_template('pages/page.html', jsonData = jsonData)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('pages/login.html')
    if "submit" in request.form:
        return redirect('/')

app.run(debug = True)