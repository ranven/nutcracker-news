from app import app
from flask import flash
from flask import render_template, request, redirect
import auth, posts, profiles, votes

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
    authenticated_user = auth.user_id()
    if request.method == "GET":
        all_posts = posts.get_all_posts(authenticated_user)

        return render_template("posts.html", posts=all_posts)
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if posts.submit_post(title, content, authenticated_user):
            flash("Post successfully created!")
            return redirect("/posts")
        else:
            flash("You need an account to post.")
            return redirect("login")
        
@app.route("/users/<user_id>", methods=["POST", "GET"])
def profile(user_id):
    authenticated_user = auth.user_id()
    is_admin = False

    if int(user_id) == authenticated_user:
        is_admin = True
        
    if request.method == "GET":
        profile = profiles.get_profile(user_id)
        users_posts = posts.get_users_posts(user_id)
        return render_template("profile.html", profile=profile, posts=users_posts, admin=is_admin)
    
    if request.method == "POST":
        if is_admin:
            description = request.form["description"]
            country = request.form["country"]
            if profiles.update_profile(description, country):
                flash("Profile successfully updated!")
                return redirect("/users/{user_id}")
        else:
            flash("You cannot edit someone else's profile.")
            return redirect("/posts")

@app.route("/likes", methods=["POST"])
def send_vote():
    authenticated_user = auth.user_id()
    post_id = request.form["post_id"]
    vote_code = True if request.form["vote_button"] == "+1" else False
    if votes.send_vote(authenticated_user, post_id, vote_code):
        return redirect('/posts') 
    else:
        flash("err")
        return redirect('/posts')

#todo: refactor flash messages and error handling, currently buggy