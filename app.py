from flask import Flask, flash
from flask import render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URL")
db = SQLAlchemy(app)

file = open('schema.sql', 'r')
schema = file.read()
file.close()

app.app_context().push()
db.session.execute(text(schema))
db.session.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
        
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT user_id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone() 

    if not user:
        flash("There's no user associated with this username. Perhaps you meant to sign up instead?")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            flash("Login successful...")
            session["username"] = username
            return redirect("/")
        else:
            flash("Invalid password or username.")
    return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        flash("An error occurred. Please try again")
        return redirect("/signup")
    else:
        session["username"] = username
        return redirect("/")
    
