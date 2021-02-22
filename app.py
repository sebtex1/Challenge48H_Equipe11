from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__) 

@app.route("/") 
def home(): 
    return render_template('pages/page.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('pages/login.html')
    if "submit" in request.form:
        return redirect('/')
app.run(debug = True)