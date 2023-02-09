from flask import Flask, flash
from flask import render_template, request, redirect
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import auth, db, posts, profiles

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if auth.login(username, password):
            flash("Login successful...")
            return redirect("/posts")
        else:
            flash("Invalid password or username.")
            redirect("/login")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if auth.signup(username, password):
            profiles.create_profile()
            flash("Successfully signed up!")
            return redirect("/posts") 
        else:
            flash("An error occurred. Please try again")
            return redirect("/signup")
    
@app.route("/logout")
def logout():
    auth.logout()
    return redirect("/")

@app.route("/posts", methods=["POST", "GET"])
def post():
    if request.method == "GET":
        all_posts = posts.get_all_posts()
        return render_template("posts.html", posts=all_posts)
    
    if request.method == "POST":
        user_id = auth.user_id()
        title = request.form["title"]
        content = request.form["content"]
        if posts.submit_post(title, content, user_id):
            flash("Post successfully created!")
            return redirect("/posts")
        else:
            flash("You need an account to post.")
            return redirect("login")
        
@app.route("/me", methods=["POST", "GET"])
def me():
    if request.method == "GET":
        user_id = auth.user_id()
        if user_id == 0:
            flash("You need an account to have a profile.")
            return redirect("login")
        profile = profiles.get_profile()
        users_posts = posts.get_users_posts()
        return render_template("profile.html", profile=profile, posts=users_posts)
    
    if request.method == "POST":
        description = request.form["description"]
        country = request.form["country"]
        if profiles.update_profile(description, country):
            flash("Profile successfully updated!")
            return redirect("/me")
        else:
            flash("You need an account to do this.")
            return redirect("login")

#todo: move routes to own module
#todo: refactor flash messages and error handling, currently buggy