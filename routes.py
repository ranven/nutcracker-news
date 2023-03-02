from app import app
from flask import flash
from flask import render_template, request, redirect
import auth, posts, profiles, votes, comments

@app.route("/")
def index():
    return redirect("/posts")

#auth
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

#posts
@app.route("/posts", methods=["POST", "GET"])
def post():
    authenticated_user = auth.user_id()
    if request.method == "GET":
        if request.args.get("sort_by"):
            sort_param = request.args.get("sort_by")
        else: 
            sort_param = "new"
        all_posts = posts.get_all_posts(authenticated_user, sort_param)
        return render_template("posts.html", posts=all_posts, sort_by=sort_param)
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if posts.submit_post(title, content, authenticated_user):
            flash("Post successfully created!")
            return redirect("/posts")
        else:
            flash("You need an account to post.")
            return redirect("login")
        
@app.route("/posts/<post_id>", methods=["GET"])
def get_post(post_id):
    authenticated_user = auth.user_id()
    post = posts.get_post(authenticated_user, post_id)
    post_comments = comments.get_comments(post_id)
    return render_template("post.html", post=post, post_comments=post_comments)

@app.route("/posts/create", methods=["GET"])
def create_post():
    if request.method == "GET":
        return render_template("create.html")
        
#comments
@app.route("/posts/<post_id>/comments", methods=["POST"])
def send_comment(post_id):
    authenticated_user = auth.user_id()
    content = request.form["content"]
    if comments.send_comment(authenticated_user, post_id, content):
        flash("Comment sent!")
        return redirect("/posts/"+post_id)
    else:
        flash("You need an account to comment.")
        return redirect("login")

#profiles     
@app.route("/users/<user_id>", methods=["POST", "GET"])
def profile(user_id):
    is_admin = False
    authenticated_user = auth.user_id()

    if int(user_id) == authenticated_user:
        is_admin = True
        
    if request.method == "GET":
        profile = profiles.get_profile(user_id)
        users_posts = posts.get_users_posts(user_id)
        users_comments = comments.get_users_comments(user_id)
        return render_template("profile.html", profile=profile, posts=users_posts, comments=users_comments, admin=is_admin)
    
    if request.method == "POST":
        if is_admin:
            description = request.form["description"]
            country = request.form["country"]
            if profiles.update_profile(description, country):
                flash("Profile successfully updated!")
                return redirect("/users/"+user_id)
        else:
            flash("You cannot edit someone else's profile.")
            return redirect("/posts")

#votes
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

#edit/delete posts/comments
@app.route("/edit/<content_type>/<content_id>", methods=["GET", "POST"])
def modify_content(content_id, content_type):
    if request.method == "GET":
        if content_type == "post":
            post = posts.get_post(0, content_id)
            return render_template("edit.html", comment=None, post=post)
        elif content_type == "comment":
            comment = comments.get_comment(content_id)
            return render_template("edit.html", comment=comment, post=None)
            
    elif request.method == "POST":
        authenticated_user = auth.user_id()
        method = request.form["method"]
        match (content_type, method):
            case "post", "put":
                title = request.form["title"]
                content = request.form["content"]
                if len(content) > 0:
                    if posts.update_post(content_id, content, title, authenticated_user):
                        flash("Post updated!")
                        return redirect("/edit/post/"+content_id)
                
            case "post", "delete":
                if posts.delete_post(content_id, authenticated_user):
                    flash("Post deleted!")
                    return redirect("/users/"+str(authenticated_user))
                
            case "comment", "put":
                content = request.form["content"]
                if len(content) > 0:
                    if comments.update_comment(content_id, content, authenticated_user):
                        flash("Comment updated!")
                        return redirect("/edit/comment/"+content_id)
                    
            case "comment", "delete":
                if comments.delete_comment(content_id, authenticated_user):
                    flash("Comment deleted!")
                    return redirect("/users/"+str(authenticated_user))

#filter for timestamps
@app.template_filter('datetimeformat')
def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)

#todo: refactor flash messages and error handling, currently buggy